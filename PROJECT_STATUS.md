# NextReel — Project Status
_Last updated: 2026-04-17_

---

## What Has Been Built

### Core System
- **Django 4.2** project with apps: `movies`, `reviews`, `recommendations`, `users`, `admin_panel`
- **SVD collaborative filtering** engine (`recommendations/engine.py`) — trained on user ratings
- **MovieLens dataset** (ml-latest-small): 9,742 movies, 100,836 ratings imported into DB
- **50 Nepali movies** added with movielens_id starting at 999001 (safe range above MovieLens max of 193609)
- **Cinematic dark/warm UI** — movie cards, hero banners, genre badges, star ratings

### Movie Model
| Field | Purpose |
|---|---|
| `title`, `year` | Basic info |
| `genres` | ManyToMany to Genre |
| `description` | Plot / overview |
| `poster` | Local image file (ImageField) |
| `poster_url_external` | External URL fallback (URLField) |
| `movielens_id` | Links to MovieLens dataset |
| `avg_rating`, `total_ratings`, `total_watches` | Aggregated stats |

`poster_url` property: local file → external URL → default SVG (fallback chain)

---

## Fixes Done (This Session)

| # | Fix | File | Commit |
|---|---|---|---|
| 1 | Genre filter lost on pagination — `{{ selected_genre }}` rendered name not ID | `templates/movies/list.html` | `e307199` |
| 2 | Watch Now button unresponsive — was form POST clashing with watchlist form | `templates/movies/detail.html` | `54a4006` |
| 3 | `poster_url_external` missing from admin MovieForm | `movies/forms.py` | `359c3cf` |
| 4 | `poster_url` was a regular method, not `@property` — broke template CSS var | `movies/models.py` | `359c3cf` |
| 5 | Nested `<form>` bug — delete review form was inside review submit form | `templates/movies/detail.html` | `359c3cf` |
| 6 | Nepali movies getting wrong OMDB posters (Hollywood/Bollywood title clashes) | DB + local files | manual |
| 7 | Junk genres injected (Biography, News, Reality-TV) from wrong OMDB matches | DB | manual |
| 8 | movielens_id collision — Nepali IDs at 99001 clashed with MovieLens (max 193609) | import command | `4caa0e9` |

---

## Ongoing: Poster Fetching

**Current state (as of 2026-04-17):**
- Total movies: **9,792**
- With local poster: **789** (~8%)
- Still missing poster: **~9,003**

**Automated daily fetch:**
- Script: `fetch_posters_daily.bat`
- Runs via **Windows Task Scheduler** at **00:30 every night**
- Fetches up to **1,000 posters/day** (OMDB free tier limit)
- Source: OMDB API (key: `12a0641e`) using IMDB IDs from `datasets/ml-latest-small/links.csv`
- Logs to: `e:\Projects\Manoj\NextReel\poster_fetch.log`

**Estimated completion:** ~9 more days (9,003 ÷ 1,000/day)

**Manual command to run now:**
```bash
python manage.py fetch_posters_omdb --api-key 12a0641e --limit 1000
```

**Nepali movies still missing poster (13):**
These need manual upload via the admin panel → Edit Movie → Poster field:
- Sungava Bhauju, Jerry, Sufi, A Mero Hajur
- Lalbandi, Masan, Bir Bikram 3, Ninu
- Swasni Manchhe Ko Laure, Guru, Mandala, Shree 3, Fighters

---

## What's Next (Planned)

### High Priority
- [ ] **Train sentiment model** — needs `imdb_reviews.csv` dataset (not present yet)
  - File needed: ~50k IMDB reviews CSV with `review` and `sentiment` columns
  - Place at: `datasets/imdb_reviews.csv`
  - Then run: `python manage.py train_sentiment`
  - Until then, sentiment badges on reviews won't appear

- [ ] **Upload missing Nepali posters** — 13 movies need manual poster upload via admin

### Medium Priority
- [ ] **Content-based filtering** — not yet implemented
  - Would recommend movies based on genre/description similarity (TF-IDF or similar)
  - Currently only SVD collaborative filtering exists
  - Useful for new users with no rating history (cold start problem)

- [ ] **Watchlist toggle state on movie list page** — the `+ Watchlist` button on list/grid cards doesn't reflect current watchlist state (unlike the detail page which does)

### Low Priority / Nice to Have
- [ ] **Movie detail page — trailer embed** — add YouTube trailer link field to Movie model
- [ ] **Search page pagination** — the advanced search page has no pagination (small result sets for now, fine)
- [ ] **Admin retrain model feedback** — retrain button works but gives no live progress indicator
- [ ] **User profile page** — watched history and watchlist tabs exist but recommendations tab could show SVD results

---

## Key Commands Reference

```bash
# Import MovieLens dataset
python manage.py import_movies

# Import Nepali movies (needs OMDB key)
python manage.py import_nepali_movies --api-key 12a0641e

# Fetch posters from OMDB (1000/day free)
python manage.py fetch_posters_omdb --api-key 12a0641e --limit 1000

# Retrain SVD model
python manage.py train_svd

# Run development server
python manage.py runserver
```

---

## Architecture Quick Reference

```
NextReel/
├── movies/          — Movie, Genre, Watchlist, WatchHistory models + views
├── reviews/         — Review model (rating 1-5 + text + sentiment)
├── recommendations/ — SVD engine, retrain management command
├── users/           — Auth, profile views
├── admin_panel/     — Custom admin dashboard
├── templates/       — All HTML templates
├── static/          — CSS, JS, default poster SVG
├── media/           — Uploaded/downloaded poster images
└── datasets/        — ml-latest-small/ (MovieLens CSV files)
```
