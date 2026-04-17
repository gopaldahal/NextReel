# NextReel — Complete Developer Documentation

> A full-stack movie recommendation web application built with Django, featuring SVD collaborative filtering, NLP-based sentiment analysis, and a cinematic dark/warm UI.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Database Models](#4-database-models)
5. [Application Architecture](#5-application-architecture)
6. [URL Routing](#6-url-routing)
7. [Recommendation System — SVD Algorithm](#7-recommendation-system--svd-algorithm)
8. [Sentiment Analysis — NLP Model](#8-sentiment-analysis--nlp-model)
9. [Dataset — MovieLens](#9-dataset--movielens)
10. [Poster Fetching System](#10-poster-fetching-system)
11. [Admin Panel](#11-admin-panel)
12. [User System](#12-user-system)
13. [Reviews System](#13-reviews-system)
14. [Frontend & UI](#14-frontend--ui)
15. [Management Commands Reference](#15-management-commands-reference)
16. [Configuration & Settings](#16-configuration--settings)
17. [Bug Fixes & Development History](#17-bug-fixes--development-history)
18. [Current Status & Pending Work](#18-current-status--pending-work)
19. [Setup Guide for New Developers](#19-setup-guide-for-new-developers)

---

## 1. Project Overview

**NextReel** is a movie recommendation platform that allows users to:

- Browse and search a library of **9,792 movies** (9,742 from MovieLens + 50 Nepali movies)
- Rate movies (1–5 stars) and write reviews
- Get **personalized recommendations** powered by a custom SVD collaborative filtering engine
- Maintain a **watchlist** and track **watch history**
- View **sentiment analysis badges** on reviews (positive / negative / neutral)
- Use a fully custom **admin panel** to manage movies, users, and retrain ML models

The system uses **no external recommendation library** — the SVD algorithm is implemented from scratch using NumPy.

---

## 2. Technology Stack

| Layer | Technology |
|---|---|
| Web Framework | Django 4.2 |
| Language | Python 3.10+ |
| Database | SQLite 3 (file: `db.sqlite3`) |
| ML — Recommendations | NumPy (custom SVD implementation) |
| ML — Sentiment | scikit-learn (Multinomial Naive Bayes) |
| Data Processing | pandas |
| Poster Fetching | requests + OMDB API |
| Frontend | Vanilla HTML/CSS/JS (no framework) |
| Model Persistence | pickle (.pkl files) |
| Media Storage | Local filesystem (`media/`) |
| Task Automation | Windows Task Scheduler (batch script) |

---

## 3. Project Structure

```
NextReel/
│
├── movie_project/              # Django project configuration
│   ├── settings.py             # All settings, DB config, ML model paths
│   ├── urls.py                 # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── movies/                     # Core movie app
│   ├── models.py               # Movie, Genre, Watchlist, WatchHistory
│   ├── views.py                # Home, List, Detail, Search, Watchlist, Watch
│   ├── forms.py                # MovieForm (admin), SearchForm
│   ├── urls.py                 # movies/ URL patterns
│   └── management/commands/
│       ├── import_movies.py        # Import MovieLens CSV dataset
│       ├── import_nepali_movies.py # Import 50 Nepali movies via OMDB
│       ├── fetch_posters_omdb.py   # Download poster images from OMDB
│       └── seed_demo.py            # Seed demo data for testing
│
├── reviews/                    # Review & sentiment app
│   ├── models.py               # Review model (rating, text, sentiment)
│   ├── views.py                # AddReview, DeleteReview + auto-retrain trigger
│   ├── sentiment.py            # Sentiment analysis engine (train + predict)
│   ├── forms.py                # ReviewForm
│   └── management/commands/
│       └── train_sentiment.py  # CLI command to train sentiment model
│
├── recommendations/            # Recommendation engine app
│   ├── engine.py               # SVD training + inference (pure NumPy)
│   ├── views.py                # Recommendations page (SVD or cold-start)
│   └── management/commands/
│       └── train_svd.py        # CLI command to train SVD model
│
├── users/                      # User authentication app
│   ├── models.py               # CustomUser (extends AbstractUser)
│   ├── views.py                # Register, Login, Logout, Profile, Theme
│   └── forms.py                # RegisterForm, ProfileEditForm
│
├── admin_panel/                # Custom admin dashboard
│   ├── views.py                # Dashboard, Users, Movies, Retrain
│   ├── decorators.py           # @admin_required decorator
│   └── urls.py
│
├── templates/                  # All HTML templates
│   ├── base.html               # Base layout (navbar, footer, theme)
│   ├── movies/
│   │   ├── home.html           # Homepage with featured/trending/new
│   │   ├── list.html           # Movie grid with filters & pagination
│   │   ├── detail.html         # Movie detail, reviews, related movies
│   │   └── search.html         # Advanced search with filters
│   ├── users/                  # Auth and profile templates
│   ├── recommendations/        # Recommendation page templates
│   └── admin_panel/            # Admin dashboard templates
│
├── static/                     # CSS, JS, SVG assets
│   └── images/
│       ├── default_poster.svg  # Fallback when no poster available
│       └── default_avatar.svg  # Fallback user avatar
│
├── media/                      # User-uploaded and downloaded files
│   └── movies/posters/         # Downloaded poster images
│
├── datasets/                   # Raw data files
│   └── ml-latest-small/
│       ├── movies.csv          # 9,742 movies (movieId, title, genres)
│       ├── ratings.csv         # 100,836 ratings (userId, movieId, rating)
│       └── links.csv           # IMDB/TMDB ID mappings
│
├── recommendations/ml_models/
│   └── svd_model.pkl           # Trained SVD model (generated after training)
│
├── reviews/ml_models/
│   ├── sentiment_model.pkl     # Trained Naive Bayes model
│   └── vectorizer.pkl          # CountVectorizer for text features
│
├── fetch_posters_daily.bat     # Windows batch script for Task Scheduler
├── manage.py
└── requirements.txt
```

---

## 4. Database Models

### Genre
```
Genre
├── id          (AutoField, PK)
└── name        (CharField, max_length=100, unique)
```
Ordered alphabetically. Examples: Action, Comedy, Drama, Nepali, Thriller.

---

### Movie
```
Movie
├── id                    (BigAutoField, PK)
├── title                 (CharField, max_length=300)
├── genres                (ManyToManyField → Genre)
├── year                  (IntegerField, nullable)
├── description           (TextField, blank)
├── poster                (ImageField → media/movies/posters/)
├── poster_url_external   (URLField, max_length=500, blank)
├── movielens_id          (IntegerField, unique)  ← links to MovieLens dataset
├── avg_rating            (FloatField, default=0.0)  ← recalculated on each review
├── total_ratings         (IntegerField, default=0)
└── total_watches         (IntegerField, default=0)

@property poster_url → local file → external URL → default SVG (fallback chain)
```

**movielens_id ranges:**
- 1 – 193,609 → MovieLens movies (official IDs)
- 999,001+ → Nepali/custom movies (safe range above MovieLens max)

---

### Review
```
Review
├── id           (BigAutoField, PK)
├── user         (ForeignKey → CustomUser, CASCADE)
├── movie        (ForeignKey → Movie, CASCADE)
├── rating       (IntegerField, choices 1–5)
├── review_text  (TextField)
├── sentiment    (CharField: 'positive' | 'negative' | 'neutral')
└── created_at   (DateTimeField, auto)

Constraint: unique_together(user, movie) — one review per user per movie
```

---

### Watchlist
```
Watchlist
├── id        (BigAutoField, PK)
├── user      (ForeignKey → CustomUser, CASCADE)
├── movie     (ForeignKey → Movie, CASCADE)
└── added_at  (DateTimeField, auto)

Constraint: unique_together(user, movie)
```

---

### WatchHistory
```
WatchHistory
├── id          (BigAutoField, PK)
├── user        (ForeignKey → CustomUser, CASCADE)
├── movie       (ForeignKey → Movie, CASCADE)
└── watched_at  (DateTimeField, auto)
```

---

### CustomUser
```
CustomUser (extends AbstractUser)
├── username, email, password  (from AbstractUser)
├── bio                        (TextField, blank)
├── avatar                     (ImageField → media/avatars/)
├── theme_preference           ('dark' | 'warm', default='dark')
└── is_new_user                (BooleanField, default=True)
                                ← becomes False after first rating
                                ← controls SVD vs cold-start recommendations
```

---

## 5. Application Architecture

### Request/Response Flow

```
Browser
  │
  ▼
Django URL Router (movie_project/urls.py)
  │
  ├── /                   → movies.HomeView
  ├── /movies/            → movies.MovieListView
  ├── /movies/<pk>/       → movies.MovieDetailView
  ├── /movies/search/     → movies.SearchView
  ├── /recommendations/   → recommendations.RecommendationView
  ├── /reviews/add/<pk>/  → reviews.AddReviewView
  ├── /users/             → users.* (login, register, profile)
  └── /admin-panel/       → admin_panel.* (dashboard, movies, users, retrain)
```

### App Responsibilities

| App | Responsibility |
|---|---|
| `movies` | Movie catalog, browsing, search, watchlist, watch history |
| `reviews` | User reviews, ratings, sentiment analysis integration |
| `recommendations` | SVD engine, recommendation page, cold-start fallback |
| `users` | Auth (register/login/logout), profile, theme preference |
| `admin_panel` | Staff-only dashboard: stats, movie CRUD, user management, model retraining |

---

## 6. URL Routing

### Root URLs (`movie_project/urls.py`)
| URL | View | Name |
|---|---|---|
| `/` | HomeView | `home` |
| `/movies/` | MovieListView | `movies:list` |
| `/movies/<pk>/` | MovieDetailView | `movies:detail` |
| `/movies/search/` | SearchView | `movies:search` |
| `/movies/<pk>/watchlist/` | AddToWatchlistView | `movies:watchlist` |
| `/movies/<pk>/watch/` | RecordWatchView | `movies:watch` |
| `/recommendations/` | RecommendationView | `recommendations:index` |
| `/reviews/add/<pk>/` | AddReviewView | `reviews:add` |
| `/reviews/delete/<pk>/` | DeleteReviewView | `reviews:delete` |
| `/users/register/` | RegisterView | `users:register` |
| `/users/login/` | LoginView | `users:login` |
| `/users/logout/` | LogoutView | `users:logout` |
| `/users/profile/` | ProfileView | `users:profile` |
| `/admin-panel/` | AdminDashboardView | `admin_panel:dashboard` |
| `/admin-panel/movies/` | MovieManagementView | `admin_panel:movies` |
| `/admin-panel/users/` | UserManagementView | `admin_panel:users` |
| `/admin-panel/retrain/` | RetrainView | `admin_panel:retrain` |

---

## 7. Recommendation System — SVD Algorithm

**File:** `recommendations/engine.py`

### What is SVD Collaborative Filtering?

SVD (Singular Value Decomposition) is a **matrix factorization technique** used in collaborative filtering. The core idea is:

> "Users who liked the same movies in the past will probably like similar movies in the future."

It works by decomposing a large user-movie rating matrix into smaller **latent factor matrices** that capture hidden patterns, such as genre preferences, tone preferences, and acting style preferences — without explicitly labeling them.

### The Rating Matrix Concept

Imagine a matrix where:
- **Rows** = Users
- **Columns** = Movies
- **Cells** = Rating (1–5), or blank if not rated

```
           Toy Story  Inception  The Matrix  Titanic
User 1         5          4          -          2
User 2         -          5          5          -
User 3         4          -          -          5
```

SVD fills in the blanks by learning latent factors that explain the observed ratings.

### Implementation Details

The system uses **Stochastic Gradient Descent (SGD)** to learn:

#### Hyperparameters
| Parameter | Value | Meaning |
|---|---|---|
| `n_factors` | 50 | Number of latent dimensions (hidden features) |
| `n_epochs` | 30 | Training iterations over the dataset |
| `lr` (learning rate) | 0.005 | Step size for gradient updates |
| `reg` (regularization) | 0.02 | L2 regularization to prevent overfitting |

#### What is Learned
- **`user_factors`** — shape `(n_users, 50)` — each user's taste profile in 50 dimensions
- **`item_factors`** — shape `(n_movies, 50)` — each movie's characteristics in 50 dimensions
- **`user_bias`** — per-user rating tendency (e.g., generous raters vs strict raters)
- **`item_bias`** — per-movie popularity/quality bias (e.g., blockbusters vs niche films)
- **`global_mean`** — the average rating across all reviews

#### Prediction Formula

For a given user `u` and movie `i`, the predicted rating is:

```
r̂(u, i) = global_mean + user_bias[u] + item_bias[i] + dot(user_factors[u], item_factors[i])
```

The result is clipped to `[1.0, 5.0]`.

#### SGD Update Rules (per training sample)

```python
err = actual_rating - predicted_rating

user_bias[u]   += lr * (err - reg * user_bias[u])
item_bias[i]   += lr * (err - reg * item_bias[i])
user_factors[u] += lr * (err * item_factors[i] - reg * user_factors[u])
item_factors[i] += lr * (err * user_factors[u] - reg * item_factors[i])
```

#### Inference (Getting Recommendations)

```python
def get_recommendations(user_id, n=20):
    1. Load trained model from svd_model.pkl
    2. Get user's rated movie IDs (exclude from candidates)
    3. For each unrated movie: compute predicted rating
    4. Sort by predicted rating descending
    5. Return top N Movie objects
```

#### Cold Start Problem

When a user has no ratings (`is_new_user=True`), SVD cannot make personalized recommendations. The fallback is:

```python
def get_cold_start_recommendations():
    return {
        'trending':     Movie.objects.order_by('-total_watches')[:12],
        'top_rated':    Movie.objects.order_by('-avg_rating')[:12],
        'new_releases': Movie.objects.order_by('-year', '-avg_rating')[:12],
    }
```

After the user submits their **first rating**, `is_new_user` is set to `False` and SVD kicks in on subsequent visits.

#### Auto-Retrain Trigger

Every time a new review is submitted, the system checks:

```python
total_reviews = Review.objects.count()
if total_reviews % 50 == 0:
    train_svd_model()  # Non-blocking, runs in same request
```

This keeps the model fresh as new ratings accumulate.

#### Model Storage

The model is saved as a Python pickle file:
```
recommendations/ml_models/svd_model.pkl
```

Contents:
```python
{
    'user_factors':  np.array,   # shape (n_users, 50)
    'item_factors':  np.array,   # shape (n_movies, 50)
    'user_index':    dict,       # str(user_id) → row index
    'item_index':    dict,       # str(movielens_id) → row index
    'global_mean':   float,
    'user_bias':     np.array,   # shape (n_users,)
    'item_bias':     np.array,   # shape (n_movies,)
    'n_factors':     int,        # 50
}
```

---

## 8. Sentiment Analysis — NLP Model

**File:** `reviews/sentiment.py`

### What It Does

Every time a user writes a review, the system automatically classifies the text as:
- `positive` — enthusiastic, approving language
- `negative` — critical, disapproving language
- `neutral` — mixed or uncertain tone

The result is stored in `Review.sentiment` and displayed as a colored badge on the review.

### Algorithm: Multinomial Naive Bayes

**Why Naive Bayes for text?**
- Works very well on short-to-medium text (movie reviews)
- Fast to train and predict
- Low memory footprint
- Effective even with limited training data

### Text Preprocessing Pipeline

```python
def preprocess_text(text):
    text = re.sub(r'<[^>]+>', '', text)     # 1. Remove HTML tags
    text = text.lower()                      # 2. Lowercase
    text = re.sub(r'[^a-z\s]', '', text)    # 3. Remove punctuation/numbers
    text = re.sub(r'\s+', ' ', text).strip()# 4. Normalize whitespace
    return text
```

### Feature Extraction

Uses `CountVectorizer` (Bag of Words):

```python
vectorizer = CountVectorizer(
    max_features=20000,     # Top 20k most frequent terms
    stop_words='english',   # Remove "the", "is", "a", etc.
    ngram_range=(1, 2),     # Unigrams + bigrams ("not good", "very bad")
)
```

Bigrams are critical for sentiment — "not good" should be negative, not positive.

### Training Data

Expects a CSV at `datasets/imdb_reviews.csv` with columns:
- `review` — text of the review
- `sentiment` — label: `positive`, `negative`, `pos`, `neg`, `1`, or `0`

The model accepts multiple label formats and maps them all to `positive`/`negative`.

**Dataset not yet present** — the system runs on a heuristic fallback until trained.

### Heuristic Fallback

When the ML model is not trained, a keyword-matching heuristic is used:

```python
positive_words = {'great', 'excellent', 'amazing', 'love', 'awesome', ...}
negative_words = {'bad', 'terrible', 'awful', 'boring', 'waste', ...}

pos_score = |words ∩ positive_words|
neg_score = |words ∩ negative_words|

if pos_score > neg_score → 'positive'
elif neg_score > pos_score → 'negative'
else → 'neutral'
```

### Confidence Threshold

Even with the ML model, low-confidence predictions default to neutral:
```python
if max(predict_proba()) < 0.6:
    return 'neutral'
```

### Training the Model

```bash
python manage.py train_sentiment
# or via Admin Panel → Retrain Models → Sentiment Model
```

After training, model accuracy (~85–90% on IMDB dataset) is printed and models are saved to:
```
reviews/ml_models/sentiment_model.pkl
reviews/ml_models/vectorizer.pkl
```

---

## 9. Dataset — MovieLens

**Source:** [GroupLens Research](https://grouplens.org/datasets/movielens/) — ml-latest-small

### Dataset Files

| File | Rows | Columns | Purpose |
|---|---|---|---|
| `movies.csv` | 9,742 | movieId, title, genres | Movie catalog |
| `ratings.csv` | 100,836 | userId, movieId, rating, timestamp | User ratings (1–5) |
| `links.csv` | 9,742 | movieId, imdbId, tmdbId | ID mappings for external APIs |

### How It's Imported

**Command:** `python manage.py import_movies`

Process:
1. Read `movies.csv` — parse title (strip year from parentheses), extract year, split pipe-separated genres
2. Read `ratings.csv` — aggregate per movie: `avg_rating = mean(ratings)`, `total_ratings = count`
3. For each movie: `Movie.objects.update_or_create(movielens_id=..., defaults={...})`
4. Create/get Genre objects, assign via `movie.genres.set(...)`

### Nepali Movies

**Command:** `python manage.py import_nepali_movies --api-key YOUR_KEY`

- 50 popular Nepali movies hardcoded with IMDB IDs
- Fetches metadata (plot, genres) from OMDB API
- Downloads poster images directly to `media/movies/posters/`
- Assigns `movielens_id` starting at 999,001 (safe range)
- Assigns "Nepali" genre to all, plus additional genres from OMDB

### Genre List (from MovieLens + Nepali)

Action, Adventure, Animation, Children, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror, IMAX, Musical, Mystery, Nepali, Romance, Sci-Fi, Thriller, War, Western

---

## 10. Poster Fetching System

Movie posters are sourced and stored through a multi-layer system.

### Poster Resolution Order (`poster_url` property)

```
1. movie.poster           → Local file in media/movies/posters/
2. movie.poster_url_external → External URL (Wikipedia, IMDB, etc.)
3. /static/images/default_poster.svg → Gray placeholder
```

### Automated OMDB Fetch

**Command:** `python manage.py fetch_posters_omdb --api-key KEY --limit 1000`

**File:** `movies/management/commands/fetch_posters_omdb.py`

Process:
1. Load `datasets/ml-latest-small/links.csv` → build `movielens_id → imdbId` map
2. Query movies with empty `poster` field
3. For each movie: call OMDB API with `?i=tt{imdbId}`
4. If poster URL returned: download image → save to `media/movies/posters/{pk}_{title}.jpg`
5. Update `Movie.poster` field via `Movie.objects.filter(pk=...).update(poster=...)`

**OMDB Free Tier:** 1,000 requests/day

### Windows Task Scheduler (Automated Daily Run)

**Script:** `fetch_posters_daily.bat`

```batch
@echo off
cd /d "e:\Projects\Manoj\NextReel"
call venv\Scripts\activate.bat
python manage.py fetch_posters_omdb --api-key 12a0641e --limit 1000 >> poster_fetch.log 2>&1
```

- Runs every night at **00:30**
- Logs to `poster_fetch.log`
- Continues from where it left off (skips movies with existing posters)

### Current Poster Status (as of 2026-04-17)

| Category | Count |
|---|---|
| Total movies | 9,792 |
| With local poster | 789 (8%) |
| Missing poster | ~9,003 |
| Estimated days to complete | ~9 days |

### Nepali Movies Missing Posters (manual upload needed)

Sungava Bhauju, Jerry, Sufi, A Mero Hajur, Lalbandi, Masan, Bir Bikram 3, Ninu, Swasni Manchhe Ko Laure, Guru, Mandala, Shree 3, Fighters

**How to upload manually:** Admin Panel → Movies → Edit → Poster field

---

## 11. Admin Panel

**URL:** `/admin-panel/`  
**Access:** Staff users only (`@admin_required` decorator checks `request.user.is_staff`)

### Dashboard (`/admin-panel/`)

Displays:
- Total users, movies, reviews
- Review sentiment breakdown (positive/negative/neutral counts)
- Top 10 movies by avg rating
- Recent 10 users and reviews

### Movie Management (`/admin-panel/movies/`)

- List all movies with search and genre filter
- Add new movie (`/admin-panel/movies/add/`)
- Edit existing movie (`/admin-panel/movies/<pk>/edit/`)
- Delete movie (`/admin-panel/movies/<pk>/delete/`)

**MovieForm fields:**
- title, genres (multi-select), year, description
- poster (file upload), poster_url_external (URL)
- movielens_id

### User Management (`/admin-panel/users/`)

- List all users with search
- Toggle user active/inactive status
- Toggle user staff status
- Protection: cannot deactivate self, cannot demote superusers

### Model Retraining (`/admin-panel/retrain/`)

Two independent checkboxes:

**SVD Model:**
- Reads all Reviews from DB
- Trains full SVD from scratch
- Saves to `recommendations/ml_models/svd_model.pkl`
- Shows success/warning/error result

**Sentiment Model:**
- Reads CSV dataset (default: `datasets/imdb_reviews.csv`)
- Trains Naive Bayes classifier
- Saves model + vectorizer to `reviews/ml_models/`
- Shows accuracy percentage

---

## 12. User System

**App:** `users/`

### Registration

- Custom `RegisterForm` extends `UserCreationForm`
- Creates `CustomUser` with `is_new_user=True`
- Auto-login after registration
- Redirects to homepage

### Authentication

- Standard Django `AuthenticationForm`
- `?next=` URL parameter preserved for redirect after login
- GET logout supported (in addition to POST) for convenience

### Profile Page (`/users/profile/`)

Three tabs:
1. **Reviews** — last 20 reviews with star ratings
2. **Watchlist** — last 20 watchlisted movies
3. **Watch History** — last 20 watched movies

Also shows: total review count, positive/negative sentiment counts.

### Theme Preference

Users can switch between:
- **Cinematic Dark** — near-black background, warm gold/amber accents
- **Warm Glow** — lighter warm-toned variant

Theme is persisted to `CustomUser.theme_preference` via AJAX POST to `/users/theme/`.

---

## 13. Reviews System

**App:** `reviews/`

### Adding a Review

1. User fills star-rating picker + textarea on movie detail page
2. POST to `/reviews/add/<movie_id>/`
3. `AddReviewView`:
   - If user already has a review for this movie → **update** (enforces one review per user per movie)
   - Otherwise → **create**
   - Runs `analyze_sentiment(review_text)` → stores result in `Review.sentiment`
   - Calls `_update_movie_rating(movie)` → recalculates `Movie.avg_rating` and `total_ratings`
   - Sets `user.is_new_user = False` (enables SVD recommendations)
   - Checks if total reviews is multiple of 50 → auto-retrain SVD

### Deleting a Review

- Owner or staff can delete
- After deletion: `_update_movie_rating(movie)` recalculates stats
- Redirects back to movie detail

### Rating Recalculation

```python
def _update_movie_rating(movie):
    stats = Review.objects.filter(movie=movie).aggregate(
        avg=Avg('rating'),
        count=Count('id'),
    )
    movie.avg_rating = round(stats['avg'] or 0.0, 2)
    movie.total_ratings = stats['count'] or 0
    movie.save(update_fields=['avg_rating', 'total_ratings'])
```

This keeps `Movie.avg_rating` always accurate and ready for ranking/sorting.

---

## 14. Frontend & UI

**No frontend framework used** — pure HTML, CSS, and vanilla JavaScript.

### Theme System

Two CSS themes applied via class on `<body>`:
- `theme-dark` — cinematic black/charcoal with gold accents
- `theme-warm` — warm brown/amber tones

User's preference is stored in DB and applied server-side via Django template context.

### Key UI Components

| Component | Usage |
|---|---|
| `movie-card` | Movie grid/row card with poster, title, rating stars |
| `hero` / `hero--detail` | Full-width blurred-poster banner on detail page |
| `detail-tabs-section` | CSS-only tabs (radio button trick) for Reviews / Related |
| `star-rating--input` | Reverse-order CSS star picker for review form |
| `badge--genre` | Genre tag chips |
| `badge--positive/negative/neutral` | Sentiment badges on reviews |
| `filter-chip` | Genre filter pills on list page |
| `pagination` | Page navigation with ellipsis logic |

### AJAX Interactions

**Watchlist toggle** (movie list + movie detail):
```javascript
fetch(url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' }
})
.then(r => r.json())
.then(data => { /* update button text + class */ })
```

Server returns: `{ status: 'ok', in_watchlist: bool, message: string }`

**Watch Now** (movie detail):
- POST to `/movies/<pk>/watch/` via AJAX
- On success: button changes to `✓ Watched`
- Shows toast notification via `window.showToast()`

---

## 15. Management Commands Reference

| Command | Description |
|---|---|
| `python manage.py import_movies` | Import all 9,742 MovieLens movies + ratings |
| `python manage.py import_movies --limit 100` | Import first 100 only (testing) |
| `python manage.py import_nepali_movies --api-key KEY` | Import 50 Nepali movies via OMDB |
| `python manage.py fetch_posters_omdb --api-key KEY` | Fetch up to 1,000 poster images from OMDB |
| `python manage.py fetch_posters_omdb --api-key KEY --overwrite` | Re-fetch even existing posters |
| `python manage.py train_svd` | Train SVD recommendation model from DB reviews |
| `python manage.py train_sentiment` | Train sentiment classifier from IMDB CSV |
| `python manage.py seed_demo` | Seed demo users and ratings for testing |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py runserver` | Start development server |

---

## 16. Configuration & Settings

**File:** `movie_project/settings.py`

### Key Settings

```python
DEBUG = True                    # Set False in production
ALLOWED_HOSTS = ['*']           # Restrict in production
SECRET_KEY = '...'              # Change in production!

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production: collectstatic

# ML Model Paths
SVD_MODEL_PATH = BASE_DIR / 'recommendations' / 'ml_models' / 'svd_model.pkl'
SENTIMENT_MODEL_PATH = BASE_DIR / 'reviews' / 'ml_models' / 'sentiment_model.pkl'
SENTIMENT_VECTORIZER_PATH = BASE_DIR / 'reviews' / 'ml_models' / 'vectorizer.pkl'
```

### Database

SQLite (default):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For production, switch to PostgreSQL by changing ENGINE and providing credentials.

---

## 17. Bug Fixes & Development History

### Bugs Found and Fixed

| # | Bug | Root Cause | Fix |
|---|---|---|---|
| 1 | Genre filter lost on pagination | `{{ selected_genre }}` rendered genre name string, not ID | Changed to `{{ selected_genre.pk }}` in all pagination links |
| 2 | Watch Now button unresponsive | Button was inside a `<form>` tag (watchlist form), causing conflicts | Converted both Watch Now and Watchlist to standalone AJAX buttons with `data-url` and `data-csrf` attributes |
| 3 | `poster_url_external` not editable in admin | Field missing from `MovieForm.fields` list | Added to fields + widgets in `movies/forms.py` |
| 4 | CSS custom property broken for hero poster | `poster_url` was a regular method, not a `@property` — templates call it without `()` | Added `@property` decorator to `Movie.poster_url` |
| 5 | Invalid HTML — nested `<form>` | Delete review form was nested inside review submit form | Moved delete form outside submit form |
| 6 | Wrong posters on Nepali movies | OMDB matched Hollywood films with same titles (e.g., "Fighters" → Bollywood War film) | Deleted wrong local files, set correct Wikipedia URLs, pinned IMDB IDs |
| 7 | Junk genres on Nepali movies | OMDB injected Biography, News, Reality-TV from wrong title matches | Deleted junk genres from DB, reset Nepali movies to Nepali-only genre |
| 8 | movielens_id collision | Nepali movies assigned IDs starting at 99,001 but MovieLens goes up to 193,609 — caused deletion of 1,685 movies | Changed Nepali range to 999,001+ (safely above MovieLens max) |
| 9 | fetch_posters_omdb crash | `movie.save()` raised `DatabaseError` for movies that were accidentally deleted | Changed to `Movie.objects.filter(pk=movie.pk).update(poster=...)` pattern |
| 10 | Unicode terminal error on Windows | Nepali movie title "Koही Mero" had Devanagari characters, Windows terminal is CP1252 | Renamed to "Kohi Mero" (ASCII-safe) |

---

## 18. Current Status & Pending Work

### Completed Features

- [x] Full movie catalog (9,742 MovieLens + 50 Nepali = 9,792 movies)
- [x] User registration, login, logout
- [x] Movie browsing, search, genre filter, pagination
- [x] Movie detail with reviews, related movies, hero banner
- [x] Star rating input and review submission
- [x] Sentiment analysis (heuristic fallback, ML when trained)
- [x] SVD collaborative filtering recommendations
- [x] Cold-start fallback (trending/top-rated/new for new users)
- [x] Auto-retrain SVD every 50 reviews
- [x] Watchlist (AJAX toggle)
- [x] Watch history recording (AJAX)
- [x] User profile with reviews/watchlist/history tabs
- [x] Theme switching (dark/warm)
- [x] Custom admin panel (dashboard, movies CRUD, user management, model retraining)
- [x] Automated daily poster fetching via Windows Task Scheduler
- [x] Nepali movie support with dedicated "Nepali" genre

### Ongoing

- **Poster fetching** — 789/9,792 have posters (~8%). Task Scheduler runs nightly at 00:30, fetching 1,000/day. ~9 more days to complete.

### Pending / Not Yet Built

| Feature | Priority | Notes |
|---|---|---|
| Train sentiment model | High | Needs `datasets/imdb_reviews.csv`. Place file → run `python manage.py train_sentiment` |
| Upload missing Nepali posters | High | 13 movies need manual upload via Admin → Edit Movie |
| Content-based filtering | Medium | Recommend by genre/description similarity. Useful for cold-start improvement. |
| Watchlist state on list cards | Medium | `+ Watchlist` button on grid cards doesn't reflect current state (detail page does) |
| Movie trailer embed | Low | Add YouTube URL field to Movie model |
| Live retrain progress | Low | Retrain page shows result but no live progress bar during training |

---

## 19. Setup Guide for New Developers

### Prerequisites

- Python 3.10+
- pip
- Git

### Step 1: Clone and Install

```bash
git clone https://github.com/gopaldahal/NextReel.git
cd NextReel
python -m venv venv
source venv/Scripts/activate          # Windows
# source venv/bin/activate            # Linux/Mac
pip install -r requirements.txt
```

### Step 2: Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser      # Create your admin account
```

### Step 3: Import Movie Data

Place MovieLens files in `datasets/` directory:
- `datasets/movies.csv`
- `datasets/ratings.csv`
- `datasets/links.csv`

Then run:
```bash
python manage.py import_movies
```

### Step 4: Fetch Posters (Optional)

Get a free OMDB API key from [omdbapi.com](http://www.omdbapi.com/) and run:
```bash
python manage.py fetch_posters_omdb --api-key YOUR_KEY --limit 1000
```

### Step 5: Train SVD Model

After users have submitted some ratings, train the recommendation engine:
```bash
python manage.py train_svd
# or: Admin Panel → Retrain Models → SVD Model
```

### Step 6: Train Sentiment Model (Optional)

Get an IMDB reviews CSV (50k reviews), place at `datasets/imdb_reviews.csv`:
```bash
python manage.py train_sentiment
# or: Admin Panel → Retrain Models → Sentiment Model
```

### Step 7: Run the Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

### Making Someone an Admin

```bash
python manage.py shell -c "from users.models import CustomUser; u=CustomUser.objects.get(username='yourname'); u.is_staff=True; u.save()"
```

Then visit `/admin-panel/`.

### Adding Nepali Movies

```bash
python manage.py import_nepali_movies --api-key YOUR_OMDB_KEY
```

---

## Appendix: Key File Paths

| Purpose | Path |
|---|---|
| Django settings | `movie_project/settings.py` |
| Root URL config | `movie_project/urls.py` |
| Movie model | `movies/models.py` |
| SVD engine | `recommendations/engine.py` |
| Sentiment engine | `reviews/sentiment.py` |
| SVD model (trained) | `recommendations/ml_models/svd_model.pkl` |
| Sentiment model (trained) | `reviews/ml_models/sentiment_model.pkl` |
| MovieLens movies | `datasets/movies.csv` |
| MovieLens ratings | `datasets/ratings.csv` |
| IMDB ID map | `datasets/ml-latest-small/links.csv` |
| Poster images | `media/movies/posters/` |
| Daily fetch script | `fetch_posters_daily.bat` |
| Poster fetch log | `poster_fetch.log` |

---

*NextReel — Built with Django 4.2, NumPy SVD, scikit-learn NLP, and vanilla frontend.*
