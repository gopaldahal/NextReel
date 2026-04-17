import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from django.conf import settings


_svd_cache = {'data': None, 'mtime': None}


def load_svd_model():
    """Load the trained SVD model, caching it in memory. Reloads if file changes."""
    model_path = settings.SVD_MODEL_PATH
    if not os.path.exists(model_path):
        return None
    mtime = os.path.getmtime(model_path)
    if _svd_cache['data'] is None or mtime != _svd_cache['mtime']:
        with open(model_path, 'rb') as f:
            _svd_cache['data'] = pickle.load(f)
        _svd_cache['mtime'] = mtime
    return _svd_cache['data']


def get_recommendations(user_id, n=20):
    """
    Get top-N movie recommendations for a user using SVD collaborative filtering.
    Returns a list of Movie objects ordered by predicted rating descending.
    Falls back to top-rated movies if SVD model is unavailable.
    """
    from movies.models import Movie
    from reviews.models import Review

    model_data = load_svd_model()
    if model_data is None:
        return list(Movie.objects.order_by('-avg_rating').prefetch_related('genres')[:n])

    try:
        user_factors = model_data['user_factors']
        item_factors = model_data['item_factors']
        user_index = model_data['user_index']
        item_index = model_data['item_index']
        global_mean = model_data['global_mean']
        user_bias = model_data['user_bias']
        item_bias = model_data['item_bias']

        str_user_id = str(user_id)
        if str_user_id not in user_index:
            return list(Movie.objects.order_by('-avg_rating').prefetch_related('genres')[:n])

        uidx = user_index[str_user_id]
        u_vec = user_factors[uidx]
        u_bias = user_bias[uidx]

        # Get movies the user hasn't rated
        rated_movie_ids = set(
            Review.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
        )
        candidate_movies = list(Movie.objects.exclude(id__in=rated_movie_ids).prefetch_related('genres'))

        if not candidate_movies:
            return list(Movie.objects.order_by('-avg_rating').prefetch_related('genres')[:n])

        predictions = []
        for movie in candidate_movies:
            str_item = str(movie.movielens_id)
            if str_item in item_index:
                iidx = item_index[str_item]
                pred = global_mean + u_bias + item_bias[iidx] + np.dot(u_vec, item_factors[iidx])
                pred = float(np.clip(pred, 1.0, 5.0))
            else:
                pred = movie.avg_rating
            predictions.append((movie, pred))

        predictions.sort(key=lambda x: x[1], reverse=True)
        return [movie for movie, _ in predictions[:n]]

    except Exception:
        return list(Movie.objects.order_by('-avg_rating').prefetch_related('genres')[:n])


def get_cold_start_recommendations(n=12):
    """
    For new or anonymous users: return trending, top-rated, and new releases.
    """
    from movies.models import Movie
    return {
        'trending': list(Movie.objects.order_by('-total_watches').prefetch_related('genres')[:n]),
        'top_rated': list(Movie.objects.order_by('-avg_rating').prefetch_related('genres')[:n]),
        'new_releases': list(Movie.objects.order_by('-year', '-avg_rating').prefetch_related('genres')[:n]),
    }


def train_svd_model():
    """
    Train SVD collaborative filtering model using numpy matrix factorization.
    Uses SGD to learn user/item latent factors + biases.
    Saves model to SVD_MODEL_PATH.
    """
    from reviews.models import Review

    print('Loading ratings from database...')
    reviews_qs = Review.objects.all().values('user_id', 'movie__movielens_id', 'rating')

    if not reviews_qs.exists():
        print('No reviews in database. Please add some ratings first.')
        return None

    df = pd.DataFrame(list(reviews_qs))
    df.columns = ['user_id', 'item_id', 'rating']
    df['user_id'] = df['user_id'].astype(str)
    df['item_id'] = df['item_id'].astype(str)
    df['rating'] = df['rating'].astype(float)

    n_users = df['user_id'].nunique()
    n_items = df['item_id'].nunique()
    print(f'Training SVD on {len(df)} ratings, {n_users} users, {n_items} movies...')

    # Build index maps
    user_index = {u: i for i, u in enumerate(df['user_id'].unique())}
    item_index = {it: i for i, it in enumerate(df['item_id'].unique())}

    # Hyperparameters
    n_factors = 50
    n_epochs = 30
    lr = 0.005
    reg = 0.02

    global_mean = float(df['rating'].mean())

    # Initialize factors and biases
    rng = np.random.RandomState(42)
    user_factors = rng.normal(0, 0.1, (len(user_index), n_factors))
    item_factors = rng.normal(0, 0.1, (len(item_index), n_factors))
    user_bias = np.zeros(len(user_index))
    item_bias = np.zeros(len(item_index))

    # SGD training
    rows = df[['user_id', 'item_id', 'rating']].values
    for epoch in range(n_epochs):
        np.random.shuffle(rows)
        total_loss = 0.0
        for row in rows:
            uid, iid, r = str(row[0]), str(row[1]), float(row[2])
            u = user_index[uid]
            i = item_index[iid]

            pred = global_mean + user_bias[u] + item_bias[i] + np.dot(user_factors[u], item_factors[i])
            err = r - pred
            total_loss += err ** 2

            # Update biases
            user_bias[u] += lr * (err - reg * user_bias[u])
            item_bias[i] += lr * (err - reg * item_bias[i])

            # Update latent factors
            uf_old = user_factors[u].copy()
            user_factors[u] += lr * (err * item_factors[i] - reg * user_factors[u])
            item_factors[i] += lr * (err * uf_old - reg * item_factors[i])

        rmse = np.sqrt(total_loss / len(rows))
        if (epoch + 1) % 5 == 0:
            print(f'  Epoch {epoch + 1}/{n_epochs} — RMSE: {rmse:.4f}')

    model_data = {
        'user_factors': user_factors,
        'item_factors': item_factors,
        'user_index': user_index,
        'item_index': item_index,
        'global_mean': global_mean,
        'user_bias': user_bias,
        'item_bias': item_bias,
        'n_factors': n_factors,
    }

    model_dir = Path(settings.SVD_MODEL_PATH).parent
    model_dir.mkdir(parents=True, exist_ok=True)
    with open(settings.SVD_MODEL_PATH, 'wb') as f:
        pickle.dump(model_data, f)

    # Invalidate in-memory cache so next request loads the new model
    _svd_cache['data'] = None
    _svd_cache['mtime'] = None

    print(f'SVD model saved to {settings.SVD_MODEL_PATH}')
    return model_data
