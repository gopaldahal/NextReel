import os
import pickle
import re
from pathlib import Path

import numpy as np
from django.conf import settings


def preprocess_text(text):
    """Remove HTML tags, lowercase, remove special characters."""
    text = re.sub(r'<[^>]+>', '', text)  # remove HTML tags
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_sentiment_model():
    """Load trained model and vectorizer from pkl files."""
    model_path = settings.SENTIMENT_MODEL_PATH
    vectorizer_path = settings.SENTIMENT_VECTORIZER_PATH
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        return None, None
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer


def analyze_sentiment(text):
    """Returns 'positive', 'negative', or 'neutral'."""
    model, vectorizer = load_sentiment_model()
    if model is None:
        # Fallback: simple heuristic when model not available
        return _heuristic_sentiment(text)
    try:
        processed = preprocess_text(text)
        features = vectorizer.transform([processed])
        prediction = model.predict(features)[0]
        proba = model.predict_proba(features)[0]
        confidence = max(proba)
        if confidence < 0.6:
            return 'neutral'
        return prediction
    except Exception:
        return 'neutral'


def _heuristic_sentiment(text):
    """Simple heuristic fallback when ML model is not available."""
    positive_words = {
        'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'brilliant',
        'love', 'loved', 'awesome', 'outstanding', 'superb', 'perfect', 'best',
        'good', 'enjoy', 'enjoyed', 'recommend', 'beautiful', 'masterpiece',
    }
    negative_words = {
        'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'hated',
        'boring', 'disappointing', 'disappointed', 'waste', 'poor', 'weak',
        'dull', 'stupid', 'annoying', 'mediocre', 'overrated', 'avoid',
    }
    text_lower = text.lower()
    words = set(re.findall(r'\b\w+\b', text_lower))
    pos_score = len(words & positive_words)
    neg_score = len(words & negative_words)
    if pos_score > neg_score:
        return 'positive'
    elif neg_score > pos_score:
        return 'negative'
    return 'neutral'


def train_sentiment_model(dataset_path):
    """
    Train Naive Bayes sentiment classifier on IMDB dataset.
    dataset_path: path to CSV with columns 'review' and 'sentiment'.
    Returns accuracy score or None on failure.
    """
    import pandas as pd
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    print(f'Loading dataset from {dataset_path}...')
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f'Dataset not found at {dataset_path}')
        return None
    except Exception as e:
        print(f'Error loading dataset: {e}')
        return None

    # Handle different column names
    if 'review' not in df.columns:
        text_col = df.columns[0]
    else:
        text_col = 'review'
    if 'sentiment' not in df.columns:
        label_col = df.columns[1]
    else:
        label_col = 'sentiment'

    print(f'Using columns: text="{text_col}", label="{label_col}"')
    df = df.dropna(subset=[text_col, label_col])
    df[text_col] = df[text_col].apply(preprocess_text)

    # Map labels to standard
    label_map = {
        'positive': 'positive',
        'negative': 'negative',
        'pos': 'positive',
        'neg': 'negative',
        '1': 'positive',
        '0': 'negative',
    }
    df[label_col] = df[label_col].astype(str).str.lower().map(label_map)
    df = df.dropna(subset=[label_col])

    if len(df) < 10:
        print('Not enough data to train. Need at least 10 samples.')
        return None

    print(f'Training on {len(df)} samples...')
    X_train, X_test, y_train, y_test = train_test_split(
        df[text_col], df[label_col], test_size=0.2, random_state=42
    )

    vectorizer = CountVectorizer(max_features=20000, stop_words='english', ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = MultinomialNB(alpha=0.5)
    model.fit(X_train_vec, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test_vec))
    print(f'Sentiment model accuracy: {accuracy:.4f}')

    # Save models
    model_dir = Path(settings.SENTIMENT_MODEL_PATH).parent
    model_dir.mkdir(parents=True, exist_ok=True)
    with open(settings.SENTIMENT_MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(settings.SENTIMENT_VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)

    print('Sentiment model saved.')
    return accuracy
