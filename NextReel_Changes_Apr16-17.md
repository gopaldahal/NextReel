# NextReel — Changes & Fixes Log
**Period: 16 April 2026 – 17 April 2026**

---

## Overview

6 commits were made across two days covering bug fixes, new features, and system-wide improvements across security, performance, UX, and code quality.

| Date | Commit | Type | Summary |
|---|---|---|---|
| 16 Apr | `4caa0e9` | Feature | OMDB poster fetch, Nepali movies, external poster URL |
| 16 Apr | `e307199` | Bug Fix | Genre filter lost on pagination |
| 17 Apr | `b4cacb7` | Feature | Automated daily poster fetch via Task Scheduler |
| 17 Apr | `54a4006` | Bug Fix | Watch Now button unresponsive |
| 17 Apr | `359c3cf` | Bug Fix | poster_url @property, nested form, admin form field |
| 17 Apr | `013ff27` | Improvement | Security, performance, UX, code quality |

---

## 16 April 2026

---

### Feature: OMDB Poster Fetch, Nepali Movies, External Poster URL
**Commit:** `4caa0e9`

#### What was added

**New field on Movie model:**
- `poster_url_external` — a URLField (max 500 chars) to store an external image URL as a fallback when no local poster file exists.

**Poster fallback chain** (`Movie.poster_url`):
```
1. Local file (media/movies/posters/)
2. poster_url_external (Wikipedia, IMDB, etc.)
3. /static/images/default_poster.svg
```

**New management command: `fetch_posters_omdb`**
- File: `movies/management/commands/fetch_posters_omdb.py`
- Fetches poster images from OMDB API using IMDB IDs from `datasets/ml-latest-small/links.csv`
- Downloads images to `media/movies/posters/`
- Updates `Movie.poster` field in the database
- Free OMDB tier: 1,000 requests/day
- Usage:
  ```bash
  python manage.py fetch_posters_omdb --api-key YOUR_KEY --limit 1000
  ```

**New management command: `import_nepali_movies`**
- File: `movies/management/commands/import_nepali_movies.py`
- Imports 50 popular Nepali movies with hardcoded IMDB IDs
- Fetches metadata (plot, genres) and poster images from OMDB
- Assigns movielens_id starting at 999,001 (safe range above MovieLens max of 193,609)
- Assigns "Nepali" genre to all movies
- Usage:
  ```bash
  python manage.py import_nepali_movies --api-key YOUR_KEY
  ```

**New management command: `fetch_posters`**
- File: `movies/management/commands/fetch_posters.py`
- Fetches poster URLs from TMDB API (requires separate TMDB API key)

**Database migration created:**
- `movies/migrations/0003_movie_poster_url_external.py`

#### Files changed
| File | Change |
|---|---|
| `movies/models.py` | Added `poster_url_external` field |
| `movies/migrations/0003_movie_poster_url_external.py` | New migration |
| `movies/management/commands/fetch_posters_omdb.py` | New command |
| `movies/management/commands/fetch_posters.py` | New command |
| `movies/management/commands/import_nepali_movies.py` | New command |
| `requirements.txt` | Added `requests` |

---

### Bug Fix: Genre Filter Lost on Pagination
**Commit:** `e307199`

#### Problem
When browsing movies filtered by a genre and clicking to page 2, 3, etc., the genre filter was silently dropped. All movies appeared instead of the filtered set.

#### Root Cause
The pagination links used `{{ selected_genre }}` which rendered as the genre's **name string** (e.g. `"Action"`) instead of its numeric ID. The view's filter logic expects an integer ID (`?genre=1`), so passing a name string caused the filter to fail silently.

**Before (broken):**
```html
<a href="?page={{ num }}&genre={{ selected_genre }}">
<!-- Rendered as: ?page=2&genre=Action  ← view ignores this -->
```

**After (fixed):**
```html
<a href="?page={{ num }}&genre={{ selected_genre.pk }}">
<!-- Renders as: ?page=2&genre=3  ← view filters correctly -->
```

#### Files changed
| File | Lines changed |
|---|---|
| `templates/movies/list.html` | All 5 pagination link `&genre=` references updated to use `.pk` |

---

## 17 April 2026

---

### Feature: Automated Daily Poster Fetch (Windows Task Scheduler)
**Commit:** `b4cacb7`

#### What was added
A Windows batch script that runs the OMDB poster fetch command automatically every night.

**File:** `fetch_posters_daily.bat`
```bat
@echo off
cd /d "e:\Projects\Manoj\NextReel"
call venv\Scripts\activate.bat
python manage.py fetch_posters_omdb --api-key 12a0641e --limit 1000 >> poster_fetch.log 2>&1
```

**Setup:** Configured in Windows Task Scheduler to run at **00:30 every night**.

- Fetches up to 1,000 posters per run (OMDB free tier daily limit)
- Logs all output to `poster_fetch.log`
- Automatically skips movies that already have a poster (only processes missing ones)
- No manual intervention needed

**Current poster status:** ~789 of 9,792 movies have posters. Completes in approximately 9 more days.

#### Files changed
| File | Change |
|---|---|
| `fetch_posters_daily.bat` | New file |

---

### Bug Fix: Watch Now Button Unresponsive
**Commit:** `54a4006`

#### Problem
Clicking "Watch Now" on the movie detail page appeared to do nothing visually, even though the watch was being recorded in the database. The watchlist button had the same issue — it was toggling but the page did not reflect the change.

#### Root Cause
Both the Watch Now and Watchlist buttons were rendered as `<button type="submit">` elements inside standard `<form>` tags. Because they were on the same page, form submissions were conflicting and causing the page to reload in unexpected ways, losing the state feedback.

#### Fix
Converted both buttons to AJAX-driven standalone buttons. They no longer rely on form submission.

**Watch Now button (before):**
```html
<form method="post" action="{% url 'movies:watch' movie.pk %}">
  {% csrf_token %}
  <button type="submit" class="btn btn--primary">Watch Now</button>
</form>
```

**Watch Now button (after):**
```html
<button type="button" class="btn btn--primary watch-now-btn"
  data-url="{% url 'movies:watch' movie.pk %}"
  data-csrf="{{ csrf_token }}">
  ▶ Watch Now
</button>
```

JavaScript handler added in `{% block extra_js %}`:
```javascript
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.watch-now-btn');
  if (!btn) return;
  fetch(btn.dataset.url, {
    method: 'POST',
    headers: { 'X-CSRFToken': btn.dataset.csrf, 'X-Requested-With': 'XMLHttpRequest' },
  })
  .then(r => r.json())
  .then(data => {
    btn.textContent = '✓ Watched';
    if (window.showToast) showToast(data.message, 'success');
  });
});
```

Same pattern applied to the Watchlist toggle button on the detail page.

#### Files changed
| File | Change |
|---|---|
| `templates/movies/detail.html` | Converted Watch Now and Watchlist to AJAX buttons |

---

### Bug Fix: Three Code Fixes (poster_url, nested form, admin form)
**Commit:** `359c3cf`

#### Fix 1 — `poster_url` Missing `@property` Decorator
**File:** `movies/models.py`

`poster_url` was defined as a regular method but used in templates as `{{ movie.poster_url }}` (without parentheses). Django templates call `@property` methods automatically but do not call regular methods without `()`. This caused the hero banner CSS custom property on the detail page to silently fail.

```python
# Before
def poster_url(self):
    ...

# After
@property
def poster_url(self):
    ...
```

---

#### Fix 2 — Nested `<form>` on Movie Detail Page
**File:** `templates/movies/detail.html`

The "Delete Review" form was nested inside the "Submit Review" form — invalid HTML. Browsers handle this inconsistently and it caused the delete action to break in some cases.

```html
<!-- Before (invalid) -->
<form method="post" action="{% url 'reviews:add' movie.pk %}">
  ...
  <form method="post" action="{% url 'reviews:delete' ... %}">  ← NESTED: invalid
    <button>Delete</button>
  </form>
</form>

<!-- After (valid) -->
<form method="post" action="{% url 'reviews:add' movie.pk %}">
  ...
  <button type="submit">Submit Review</button>
</form>
<form method="post" action="{% url 'reviews:delete' ... %}">  ← outside, valid
  <button type="submit">Delete Review</button>
</form>
```

---

#### Fix 3 — `poster_url_external` Missing from Admin Movie Form
**File:** `movies/forms.py`

The `poster_url_external` field (added to the Movie model in the 16 Apr commit) was not included in `MovieForm`, so admins had no way to set external poster URLs via the admin panel.

```python
# Added to MovieForm.Meta.fields and widgets
fields = ['title', 'genres', 'year', 'description', 'poster', 'poster_url_external', 'movielens_id']
widgets = {
    ...
    'poster_url_external': forms.URLInput(attrs={
        'class': 'form-input',
        'placeholder': 'https://example.com/poster.jpg'
    }),
}
```

#### Files changed
| File | Change |
|---|---|
| `movies/models.py` | Added `@property` to `poster_url` |
| `movies/forms.py` | Added `poster_url_external` to `MovieForm` |
| `templates/movies/detail.html` | Moved delete review form outside submit form |

---

### Improvement: Security, Performance, UX & Code Quality
**Commit:** `013ff27`

#### Security

**Environment variables for sensitive config** (`movie_project/settings.py`)

Sensitive values are no longer hardcoded. They read from environment variables with safe development defaults.

| Setting | Before | After |
|---|---|---|
| `SECRET_KEY` | Hardcoded string | `os.environ.get('DJANGO_SECRET_KEY', fallback)` |
| `DEBUG` | `True` hardcoded | `os.environ.get('DJANGO_DEBUG', 'True') == 'True'` |
| `ALLOWED_HOSTS` | `['*']` hardcoded | `os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')` |

Email settings (for password reset) also read from env vars.

New file `.env.example` documents all available variables for developers.

---

#### Performance

**SVD and Sentiment models cached in memory**

Both `load_svd_model()` and `load_sentiment_model()` previously re-read the pickle file from disk on every single call. With 9,000+ movies and 50 latent factors, this added measurable overhead to every recommendations page load and every review submission.

Fix: module-level dict cache with mtime-based invalidation. The model is loaded once and reused. If the `.pkl` file is replaced (after retraining), the next call detects the changed mtime and reloads automatically.

```python
_svd_cache = {'data': None, 'mtime': None}

def load_svd_model():
    mtime = os.path.getmtime(model_path)
    if _svd_cache['data'] is None or mtime != _svd_cache['mtime']:
        with open(model_path, 'rb') as f:
            _svd_cache['data'] = pickle.load(f)
        _svd_cache['mtime'] = mtime
    return _svd_cache['data']
```

The cache is explicitly cleared after training so the fresh model loads on the next request.

---

**N+1 query fixed on recommendations page**

The recommendation engine was calling `movie.genres.all()` inside a loop over 20 movies — generating 20 separate database queries just to display genre badges.

Fix: `prefetch_related('genres')` added to all querysets in `recommendations/engine.py` (candidate movies, all fallback queries, and cold-start queries).

| Before | After |
|---|---|
| 21+ DB queries per recommendations page | 2 DB queries |

---

**Auto-retrain SVD moved to background thread**

Every 50th review submission triggered a full SVD model retrain synchronously inside the HTTP request — blocking the user's browser for several seconds while 30 epochs of SGD ran.

Fix: runs in a daemon background thread. The review response is returned immediately.

```python
# Before — blocked the request
train_svd_model()

# After — returns instantly, trains in background
t = threading.Thread(target=train_svd_model, daemon=True)
t.start()
```

---

#### UX

**Watchlist state on movie list and recommendations pages**

The `+ Watchlist` button on movie grid cards always showed `+ Watchlist` regardless of whether the movie was already in the user's watchlist. Users had no visual feedback.

Fix: the list view and recommendations view now query the user's watchlist for the current page's movies and pass a `watchlisted_ids` set to the template. Buttons reflect the correct state on page load.

```
Before: + Watchlist  (always, even if already added)
After:  ✓ In List   (if already in watchlist)
        + Watchlist  (if not in watchlist)
```

---

**Watch Now "already watched" state**

The Watch Now button on the movie detail page showed "▶ Watch Now" even if the user had already watched the film before.

Fix: `MovieDetailView` now queries `WatchHistory` and passes `already_watched` to the template.

```
Before: ▶ Watch Now  (always)
After:  ✓ Watched   (if already in watch history)
        ▶ Watch Now  (if never watched)
```

---

**Password Reset flow**

Users who forgot their password had no way to regain access — the "Forgot password?" link pointed to `#`.

Added full Django built-in password reset flow:

| URL | Page |
|---|---|
| `/users/password-reset/` | Enter email address |
| `/users/password-reset/done/` | Confirmation: check your email |
| `/users/password-reset-confirm/<uid>/<token>/` | Set new password |
| `/users/password-reset-complete/` | Success: password updated |

In development, the reset email is printed to the terminal console (no SMTP needed). In production, configure `EMAIL_HOST`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` environment variables.

New templates created:
- `templates/users/password_reset.html`
- `templates/users/password_reset_done.html`
- `templates/users/password_reset_confirm.html`
- `templates/users/password_reset_complete.html`
- `templates/users/password_reset_email.html`
- `templates/users/password_reset_subject.txt`

---

#### Code Quality

**Removed unused `nltk` dependency**
`nltk` was listed in `requirements.txt` but never imported anywhere in the codebase. Removed.

**Standardised context variable naming**
`MovieListView` was passing both `query` and `search_query` to the template (duplicate). Removed `query`, now consistently uses `search_query` across all views.

`SearchView` was passing `selected_genre` as a raw ID string. Fixed to pass the Genre object for consistency.

**Template DRY — `_card.html` partial now actually used**
A reusable `templates/movies/_card.html` partial existed but was not used anywhere. All four places that had inline movie card HTML (`list.html`, `recommendations/index.html` — trending, top_rated, new_releases, and personalized sections) now use `{% include "movies/_card.html" %}`. This removed ~120 lines of duplicate HTML. Any future card design change only needs to be made in one file.

The partial was also updated to support `watchlisted_ids` for accurate button state and to show the numeric rating value.

#### Files changed
| File | Change |
|---|---|
| `movie_project/settings.py` | Env vars for SECRET_KEY, DEBUG, ALLOWED_HOSTS, email |
| `.env.example` | New file — documents all env var options |
| `movies/views.py` | Added `watchlisted_ids` and `already_watched` to context |
| `recommendations/engine.py` | In-memory model cache, prefetch_related on all queries |
| `recommendations/views.py` | Pass `watchlisted_ids` to context; use prefetch_related |
| `reviews/views.py` | Background thread for auto-retrain |
| `reviews/sentiment.py` | In-memory model cache for sentiment model |
| `requirements.txt` | Removed `nltk` |
| `templates/movies/_card.html` | Updated to support watchlisted_ids and rating value |
| `templates/movies/list.html` | Use `_card.html` partial (–35 lines) |
| `templates/movies/detail.html` | Watch Now shows already-watched state |
| `templates/recommendations/index.html` | Use `_card.html` partial (–120 lines) |
| `templates/users/login.html` | Forgot password link now points to real URL |
| `templates/users/password_reset*.html` | 6 new password reset templates |
| `users/urls.py` | Added 4 password reset URL patterns |

---

## Summary

| Category | Count | Items |
|---|---|---|
| Bug fixes | 5 | Genre pagination, Watch Now AJAX, poster_url @property, nested form, admin form field |
| New features | 3 | OMDB poster fetch, Nepali movie import, automated Task Scheduler |
| Performance | 3 | Model memory cache, N+1 fix, background retrain |
| Security | 1 | Env vars for all sensitive config |
| UX | 3 | Watchlist state on cards, already-watched state, password reset |
| Code quality | 3 | Remove nltk, fix context vars, use _card.html partial |
