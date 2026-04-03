# NextReel — Administrator Guide

This guide is intended for staff and superusers responsible for managing the NextReel application. It covers the custom Admin Panel, Django's built-in admin interface, data import, and machine learning model management.

---

## Table of Contents

1. [Roles and Permissions](#1-roles-and-permissions)
2. [Accessing the Admin Panel](#2-accessing-the-admin-panel)
3. [Dashboard Overview](#3-dashboard-overview)
4. [User Management](#4-user-management)
5. [Movie Management](#5-movie-management)
6. [Importing Movies from MovieLens CSV](#6-importing-movies-from-movielens-csv)
7. [Machine Learning Model Management](#7-machine-learning-model-management)
8. [Django Built-in Admin](#8-django-built-in-admin)
9. [Management Commands Reference](#9-management-commands-reference)
10. [Database and Maintenance](#10-database-and-maintenance)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Roles and Permissions

NextReel uses Django's standard permission model with two levels of elevated access:

| Role | `is_staff` | `is_superuser` | Access |
|---|---|---|---|
| Regular User | No | No | Browse, review, watchlist, recommendations. |
| Staff User | Yes | No | Custom Admin Panel (users, movies, retrain). |
| Superuser | Yes | Yes | All of the above + Django built-in `/admin/` interface. |

The custom admin panel (`/admin-panel/`) is protected by the `admin_required` decorator, which requires the user to have `is_staff = True`. Regular users who attempt to access admin URLs are redirected to the login page or shown a 403 error.

> **Important:** A superuser automatically has staff access. You do not need to set both flags.

---

## 2. Accessing the Admin Panel

### Custom Admin Panel

The custom NextReel admin dashboard is located at:

```
/admin-panel/
```

To access it:

1. Log in with a staff or superuser account.
2. Navigate to `/admin-panel/` directly, or click the **Admin Panel** link in the navigation bar (only visible to staff/superusers).

### Creating the First Superuser

If no superuser exists yet, create one from the command line:

```bash
python manage.py createsuperuser
```

You will be prompted to enter:

```
Username: admin
Email address: admin@example.com
Password: ************
Password (again): ************
Superuser created successfully.
```

### Promoting an Existing User to Staff

**Via the Custom Admin Panel:**

1. Go to `/admin-panel/users/`.
2. Find the user in the list.
3. Click **Grant Staff** (or the staff toggle button) next to their name.

**Via the Django Admin Interface:**

1. Go to `/admin/` (requires superuser).
2. Navigate to **Users** under the `USERS` section.
3. Click the username.
4. Check **Staff status** and/or **Superuser status**.
5. Click **Save**.

**Via the Command Line:**

```bash
python manage.py shell
```

```python
from users.models import CustomUser
user = CustomUser.objects.get(username='username_here')
user.is_staff = True
user.save()
```

---

## 3. Dashboard Overview

The Dashboard (`/admin-panel/`) provides a real-time summary of the platform's health.

### Statistics Cards

| Card | Description |
|---|---|
| **Total Users** | Total number of registered accounts. |
| **Total Movies** | Total number of movies in the database. |
| **Total Reviews** | Total number of reviews submitted across all movies. |
| **Positive Reviews** | Count of reviews automatically classified as positive. |
| **Negative Reviews** | Count of reviews automatically classified as negative. |
| **Neutral Reviews** | Count of reviews classified as neutral. |

### Data Tables

| Table | Description |
|---|---|
| **Top 10 Movies** | Movies ranked by average rating (with total ratings count). |
| **Recent Users** | The 10 most recently registered users (username, email, join date). |
| **Recent Reviews** | The 10 most recently submitted reviews (user, movie, rating, sentiment). |

> **Tip:** The dashboard loads live data on every page visit. There is no need to refresh manually to see new statistics.

---

## 4. User Management

Navigate to `/admin-panel/users/` to manage registered users.

### User List

The user list is paginated (25 per page) and shows:
- Username and email address.
- Date joined.
- Active status (green = active, red = deactivated).
- Staff status badge.
- Action buttons (Activate/Deactivate, Grant/Revoke Staff).

### Searching Users

Use the search bar at the top to filter users by username, email, first name, or last name.

### Activating and Deactivating Users

Deactivating a user prevents them from logging in without deleting their data.

1. Find the user in the list.
2. Click **Deactivate** (if currently active) or **Activate** (if currently deactivated).
3. A confirmation message appears and the status updates immediately.

**Restrictions:**
- You cannot deactivate your own account from the admin panel.
- Only superusers can deactivate other superusers.

### Granting and Revoking Staff Access

Staff access gives a user the ability to access the `/admin-panel/` interface.

1. Find the user in the list.
2. Click **Grant Staff** to give staff access, or **Revoke Staff** to remove it.

**Restrictions:**
- You cannot change your own staff status.
- The staff status of a superuser cannot be changed via this interface (use Django admin for superuser management).

### Understanding User Flags

| Flag | Field | Effect |
|---|---|---|
| `is_active` | Active status | If False, user cannot log in. |
| `is_staff` | Staff status | If True, user can access `/admin-panel/`. |
| `is_superuser` | Superuser status | Full unrestricted access including Django admin. |
| `is_new_user` | New user flag | If True, user sees cold-start recommendations instead of personalized SVD results. Automatically set to False after the user's first review submission. |

---

## 5. Movie Management

Navigate to `/admin-panel/movies/` to manage the movie catalog.

### Movie List

The movie list is paginated (25 per page) and shows:
- Movie title and release year.
- Genres.
- Average rating and total rating count.
- Action buttons (Edit, Delete).

### Filtering Movies

Use the search bar to filter by title or description, and the genre dropdown to filter by genre.

### Adding a Movie Manually

1. Click **Add Movie** at the top of the movie list.
2. Fill in the form:
   - **Title** (required) — The movie's full title.
   - **MovieLens ID** (required) — A unique numeric identifier. If adding a movie not from the MovieLens dataset, use any unique integer.
   - **Year** — Release year (e.g., 1994).
   - **Description** — A plot synopsis or description.
   - **Genres** — Select one or more genres from the list (hold Ctrl/Cmd to select multiple).
   - **Poster** — Upload a poster image (JPG or PNG recommended).
3. Click **Save Movie**.

> **Note:** The `movielens_id` field must be unique across all movies. If you enter a duplicate ID, the form will display a validation error.

### Editing a Movie

1. Find the movie in the list.
2. Click the **Edit** button.
3. Modify any fields in the form.
4. Click **Save Movie**.

> **Tip:** You can update the poster image by uploading a new file. The old image file is not automatically deleted from the file system.

### Deleting a Movie

1. Find the movie in the list.
2. Click the **Delete** button.
3. A confirmation page appears showing the movie title.
4. Click **Confirm Delete** to permanently remove the movie.

> **Warning:** Deleting a movie also deletes all associated reviews, watchlist entries, and watch history records due to Django's `CASCADE` delete behavior. This action cannot be undone.

---

## 6. Importing Movies from MovieLens CSV

The recommended way to populate the movie database is by importing from the MovieLens dataset CSV files. This is much faster than adding movies manually.

### Obtaining the Dataset

Download the MovieLens dataset from [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/). The **MovieLens Latest Small** or **MovieLens 25M** datasets both work.

The import command expects two files:
- `movies.csv` — columns: `movieId`, `title`, `genres` (pipe-separated, e.g., `Action|Drama`)
- `ratings.csv` — columns: `userId`, `movieId`, `rating`, `timestamp`

### Placing the Files

Place the CSV files in the `datasets/` directory at the project root:

```
NextReel/
├── datasets/
│   ├── movies.csv
│   └── ratings.csv
├── manage.py
└── ...
```

### Running the Import

```bash
python manage.py import_movies
```

This command will:
1. Read all movies from `movies.csv`.
2. Extract the year from titles formatted as `"Title (Year)"`.
3. Calculate average rating and total ratings from `ratings.csv`.
4. Create or update Genre records.
5. Create or update Movie records.

**Output example:**

```
Reading movies dataset from .../datasets/movies.csv...
Reading ratings dataset from .../datasets/ratings.csv...
Importing 9742 movies...
Import complete! Created: 9742, Updated: 0, Total movies in DB: 9742
```

### Import Options

| Option | Description | Example |
|---|---|---|
| `--movies` | Custom path to movies.csv | `--movies /path/to/movies.csv` |
| `--ratings` | Custom path to ratings.csv | `--ratings /path/to/ratings.csv` |
| `--limit` | Import only the first N movies (for testing) | `--limit 500` |

**Example with custom paths:**

```bash
python manage.py import_movies --movies /data/ml-latest/movies.csv --ratings /data/ml-latest/ratings.csv
```

**Example for a test import (first 100 movies only):**

```bash
python manage.py import_movies --limit 100
```

### Re-running the Import

The import command uses `update_or_create` on the `movielens_id` field, so it is safe to run multiple times. Existing movies will be updated with fresh data; no duplicates will be created.

> **Note:** Genre records are also deduplicated automatically using `get_or_create`.

---

## 7. Machine Learning Model Management

NextReel uses two ML models:

| Model | Purpose | File |
|---|---|---|
| SVD Collaborative Filtering | Personalized movie recommendations | `recommendations/ml_models/svd_model.pkl` |
| Naive Bayes + TF-IDF | Automatic sentiment analysis of reviews | `reviews/ml_models/sentiment_model.pkl` + `reviews/ml_models/vectorizer.pkl` |

### Automatic Retraining

The SVD model is **automatically retrained** every time the total number of reviews in the database reaches a multiple of 50 (i.e., after the 50th, 100th, 150th review, etc.). This happens in the background during review submission and does not affect the user experience.

### Manual Retraining via Admin Panel

1. Navigate to `/admin-panel/retrain/` (accessible from the Admin Panel sidebar as **Retrain Models**).
2. Check the box for the model(s) you want to retrain:
   - **Retrain SVD Model** — Uses all current review data in the database.
   - **Retrain Sentiment Model** — Requires a path to the IMDB dataset CSV.
3. If retraining the sentiment model, enter the dataset path (default: `datasets/imdb_reviews.csv`).
4. Click **Start Retraining**.
5. Results (success/failure/accuracy) are shown on the same page.

### Manual Retraining via Command Line

**Retrain SVD model:**

```bash
python manage.py train_svd
```

This reads all `Review` records from the database and trains a new SVD model. The trained model is saved to the path defined by `SVD_MODEL_PATH` in `settings.py`.

**Prerequisites:**
- At least a few hundred reviews should exist in the database for meaningful recommendations.
- `numpy` and `pandas` must be installed (included in `requirements.txt`).

**Output example:**

```
Starting SVD model training...
Loading ratings from database...
Training SVD on 100000 ratings, 943 users, 1682 movies...
  Epoch 5/30 — RMSE: 0.9821
  Epoch 10/30 — RMSE: 0.9342
  Epoch 15/30 — RMSE: 0.9101
  Epoch 20/30 — RMSE: 0.8978
  Epoch 25/30 — RMSE: 0.8904
  Epoch 30/30 — RMSE: 0.8867
SVD model saved to .../recommendations/ml_models/svd_model.pkl
SVD model training complete!
```

**Retrain Sentiment model:**

```bash
python manage.py train_sentiment
```

Or with a custom dataset path:

```bash
python manage.py train_sentiment --dataset /path/to/imdb_reviews.csv
```

**Prerequisites:**
- A CSV file with columns `review` (text) and `sentiment` (`positive` / `negative`).
- The IMDB 50K dataset from Kaggle is recommended: [https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)
- `scikit-learn` must be installed (included in `requirements.txt`).

**Output example:**

```
Training sentiment model with dataset: .../datasets/imdb_reviews.csv
Loading dataset from .../datasets/imdb_reviews.csv...
Using columns: text="review", label="sentiment"
Training on 50000 samples...
Sentiment model accuracy: 0.8712 (87.12%)
Sentiment model saved.
Training complete! Accuracy: 0.8712 (87.12%)
```

### Model File Locations

The model file paths are configured in `settings.py`:

```python
SVD_MODEL_PATH = BASE_DIR / 'recommendations' / 'ml_models' / 'svd_model.pkl'
SENTIMENT_MODEL_PATH = BASE_DIR / 'reviews' / 'ml_models' / 'sentiment_model.pkl'
SENTIMENT_VECTORIZER_PATH = BASE_DIR / 'reviews' / 'ml_models' / 'vectorizer.pkl'
```

> **Note:** If the SVD model file does not exist, the recommendation engine automatically falls back to showing top-rated movies. If the sentiment model file does not exist, the system falls back to a keyword-based heuristic classifier.

### Fallback Behavior

| Model Missing | Fallback Behavior |
|---|---|
| SVD model absent | All users see top-rated movies on the Recommendations page. |
| Sentiment model absent | Review sentiment is determined by a keyword heuristic (positive/negative word lists). |

---

## 8. Django Built-in Admin

In addition to the custom admin panel, Django's standard admin interface is available at:

```
/admin/
```

This requires a **superuser** account (not just staff).

### Accessing Django Admin

1. Navigate to `/admin/`.
2. Log in with superuser credentials.

### What You Can Do in Django Admin

- Full CRUD (Create, Read, Update, Delete) for all models: Users, Movies, Genres, Reviews, Watchlist entries, WatchHistory records.
- View and manage individual database records with fine-grained control.
- Export data, run custom actions, and inspect relationships.
- Manage Django session and authentication tokens.

> **Warning:** The Django admin interface provides direct database access. Be cautious when deleting records, as cascade deletions can remove related data permanently.

### Registering Additional Models

If you need to access a model not currently in the Django admin, add it to the relevant `admin.py` file:

```python
# Example: in movies/admin.py
from django.contrib import admin
from .models import Movie, Genre, Watchlist, WatchHistory

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Watchlist)
admin.site.register(WatchHistory)
```

---

## 9. Management Commands Reference

| Command | Description |
|---|---|
| `python manage.py createsuperuser` | Create the first superuser account interactively. |
| `python manage.py import_movies` | Import movies from `datasets/movies.csv` and `datasets/ratings.csv`. |
| `python manage.py import_movies --limit 500` | Import only the first 500 movies (for testing). |
| `python manage.py import_movies --movies <path> --ratings <path>` | Import from custom file paths. |
| `python manage.py train_svd` | Train/retrain the SVD recommendation model from current review data. |
| `python manage.py train_sentiment` | Train/retrain the sentiment analysis model from `datasets/imdb_reviews.csv`. |
| `python manage.py train_sentiment --dataset <path>` | Train sentiment model from a custom CSV file. |
| `python manage.py migrate` | Apply database migrations. |
| `python manage.py makemigrations` | Generate new migration files after model changes. |
| `python manage.py collectstatic` | Collect static files for production deployment. |
| `python manage.py runserver` | Start the development server (default: `http://127.0.0.1:8000/`). |

### First-Time Setup Sequence

Run these commands in order when setting up a fresh deployment:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py migrate

# 3. Create a superuser
python manage.py createsuperuser

# 4. Import movie data (place CSV files in datasets/ first)
python manage.py import_movies

# 5. Train the sentiment model (place IMDB CSV in datasets/ first)
python manage.py train_sentiment

# 6. Start the development server
python manage.py runserver
```

> **Note:** The SVD model cannot be trained until users have submitted reviews, so `train_svd` is typically run after the platform has been in use for some time.

---

## 10. Database and Maintenance

### Database File

NextReel uses **SQLite** as its database backend. The database is stored in a single file:

```
NextReel/db.sqlite3
```

### Backing Up the Database

To back up the database, simply copy the `db.sqlite3` file:

```bash
cp db.sqlite3 db.sqlite3.backup_$(date +%Y%m%d)
```

### Resetting the Database

> **Warning:** This permanently deletes all data.

```bash
# Delete the database file
rm db.sqlite3

# Recreate the schema
python manage.py migrate

# Recreate the superuser
python manage.py createsuperuser

# Re-import movies
python manage.py import_movies
```

### Exporting Data as JSON Fixtures

```bash
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
```

### Clearing Sessions

To clear expired session records from the database:

```bash
python manage.py clearsessions
```

### Static Files

In development, Django serves static files automatically from the `static/` directory.

In production, collect static files first:

```bash
python manage.py collectstatic
```

Static files will be copied to the `staticfiles/` directory, which your web server (e.g., nginx) should serve directly.

---

## 11. Troubleshooting

### "No reviews in database" when training SVD

The SVD model requires review data to train. Ensure that:
1. Movies have been imported (`python manage.py import_movies`).
2. Users have submitted reviews through the website.
3. At least 10–20 unique user-movie ratings exist.

### Recommendations show only top-rated movies for all users

The SVD model file is missing or corrupted. Retrain it:

```bash
python manage.py train_svd
```

Verify the model file exists at `recommendations/ml_models/svd_model.pkl`.

### Sentiment always shows "neutral"

The sentiment model is missing. Train it:

```bash
python manage.py train_sentiment
```

If the model file exists but sentiment is still always neutral, check that the review text is not too short (less than 3–4 meaningful words).

### "movies.csv not found" during import

Ensure the CSV file is placed in the `datasets/` directory at the project root, or provide the full path using the `--movies` flag.

### Static files (CSS, images) not loading

In development, ensure `DEBUG = True` in `settings.py`. If the issue persists, verify that the `static/` directory exists and contains the expected files:

```bash
python manage.py findstatic css/main.css
```

### Media files (uploaded avatars, posters) not loading

Ensure `MEDIA_URL` and `MEDIA_ROOT` are correctly configured in `settings.py`, and that the URL routing includes `static(settings.MEDIA_URL, ...)` in `urls.py`. In development this is handled automatically. In production, configure your web server to serve the `media/` directory.

### A user cannot log in (account was deactivated)

Go to `/admin-panel/users/`, find the user, and click **Activate**. Alternatively, use Django admin at `/admin/` to set `is_active = True` on the user record.

### Import creates duplicate movies

The import command deduplicates on `movielens_id`. Duplicates only occur if you have manually added movies with MovieLens IDs that conflict with the CSV data. Resolve conflicts by deleting the manually added movie before re-running the import, or by assigning a unique ID (e.g., a large number such as 999001) to manually added movies.
