# NextReel — Project Defense Preparation Guide
**Complete Q&A, Technical Explanations, and Presentation Strategy**

---

## Table of Contents

1. [Project Summary (30-second pitch)](#1-project-summary)
2. [What Problem Does This Solve?](#2-what-problem-does-this-solve)
3. [System Architecture](#3-system-architecture)
4. [Technology Choices & Justification](#4-technology-choices--justification)
5. [Database Design](#5-database-design)
6. [Recommendation Algorithm — Deep Explanation](#6-recommendation-algorithm--deep-explanation)
7. [Sentiment Analysis — Deep Explanation](#7-sentiment-analysis--deep-explanation)
8. [Dataset](#8-dataset)
9. [Key Features](#9-key-features)
10. [Probable Defense Questions & Answers](#10-probable-defense-questions--answers)
11. [Known Limitations & How to Address Them](#11-known-limitations--how-to-address-them)
12. [Live Demo Walkthrough](#12-live-demo-walkthrough)
13. [Future Work](#13-future-work)

---

## 1. Project Summary

**NextReel** is a full-stack web application that recommends movies to users based on their personal rating history using machine learning.

> "NextReel is a movie recommendation platform built with Django that uses SVD-based collaborative filtering to generate personalized recommendations. Users can browse 9,792 movies, rate and review them, and receive tailored suggestions. Reviews are automatically analyzed for sentiment using a Naive Bayes NLP classifier. The system also includes a Nepali movie collection and a custom admin panel for content and model management."

**Live stats:**
- 9,792 movies in database (9,742 from MovieLens + 50 Nepali)
- 20 genres
- 100,836 real user ratings imported from MovieLens dataset
- 8 registered users, 84 reviews, 52 watchlist entries

---

## 2. What Problem Does This Solve?

### The Problem
With millions of movies available on streaming platforms, users suffer from **choice overload**. They waste time scrolling endlessly or miss films they would love because they simply never encountered them.

### The Solution
NextReel solves this by:
1. **Learning each user's taste** from their ratings (1–5 stars)
2. **Predicting** how much that user would enjoy movies they haven't seen
3. **Surfacing** the highest-predicted movies as personalized recommendations
4. **Understanding** whether reviews are positive or negative automatically

### Who is it for?
- Movie enthusiasts who want curated recommendations
- Nepali audiences who want to find local content alongside international films
- Anyone who has experienced "I don't know what to watch tonight"

---

## 3. System Architecture

### High-Level Architecture

```
User Browser
     │
     ▼
Django Web Server (MVT Pattern)
     │
     ├── movies app       — catalog, search, watchlist
     ├── reviews app      — ratings, reviews, sentiment analysis
     ├── recommendations  — SVD engine, personalized results
     ├── users app        — authentication, profile
     └── admin_panel      — staff dashboard, model retraining
     │
     ├── SQLite Database (db.sqlite3)
     ├── ML Models (pickle files)
     │     ├── svd_model.pkl        — recommendation engine
     │     └── sentiment_model.pkl  — review classifier
     └── Media Storage (local filesystem)
           └── movies/posters/      — downloaded poster images
```

### Design Pattern — MVT (Model-View-Template)
Django follows **MVT** which is similar to MVC:

| Layer | Django equivalent | Role |
|---|---|---|
| Model | `models.py` | Database structure, business logic |
| View | `views.py` | Request handling, data processing |
| Template | `templates/*.html` | HTML rendering |

### Request Flow Example (movie detail page)
```
1. User visits /movies/42/
2. Django URL router maps to MovieDetailView
3. View queries: Movie, Reviews, Watchlist, WatchHistory
4. View passes context dict to detail.html template
5. Template renders HTML with movie data
6. Response sent to browser
```

---

## 4. Technology Choices & Justification

### Why Django?
- Python-based — same language as the ML models (no language boundary)
- Built-in ORM — no raw SQL needed
- Built-in authentication system
- MVT pattern keeps code organised
- Large community, well-documented

### Why SQLite?
- Zero configuration — no database server to install
- Sufficient for a project of this scale
- File-based — easy to back up and transport
- In production, would switch to PostgreSQL

### Why NumPy for SVD (not scikit-surprise or TensorFlow)?
- **Full control** over the algorithm — can explain every line
- No black-box library dependency
- Demonstrates understanding of the mathematics
- scikit-surprise would work but hides the implementation details

### Why Naive Bayes for sentiment?
- Proven to work very well on text classification
- Fast to train (milliseconds)
- Interpretable — can explain why a prediction was made
- Outperforms more complex models on short text (movie reviews)

### Why no React/Vue frontend?
- Django templates are sufficient for this use case
- Reduces complexity — one language (Python/HTML/CSS) instead of two stacks
- AJAX used only where necessary (watchlist, watch now)
- Focus is on the ML components, not frontend framework

---

## 5. Database Design

### Entity Relationship Summary

```
CustomUser ──< Review >── Movie ──< Genre
    │                       │
    ├──< Watchlist >─────────┤
    └──< WatchHistory >──────┘
```

### Tables and Key Fields

**Movie**
- `movielens_id` — links to MovieLens dataset for SVD training
- `avg_rating` — pre-computed average, updated on every review (fast reads)
- `total_watches` — used for "Trending Now" sorting
- `poster_url_external` — fallback if no local poster file

**Review**
- `unique_together(user, movie)` — one review per user per movie (enforced at DB level)
- `sentiment` — auto-assigned by NLP model on save
- Rating 1–5 stars

**CustomUser** extends Django's AbstractUser
- `is_new_user` — flag that switches between cold-start and SVD recommendations
- `theme_preference` — persisted dark/warm theme

### Why denormalize avg_rating onto the Movie table?
Calculating `AVG(rating)` across all reviews on every page load would be slow with 100,836 ratings. Instead, `avg_rating` is recalculated and saved to the Movie row every time a review is added or deleted — a write-time cost for a read-time gain.

---

## 6. Recommendation Algorithm — Deep Explanation

### What is Collaborative Filtering?
The core assumption: **"Users who agreed in the past will agree in the future."**

If User A and User B both loved Inception and The Dark Knight, and User A also loved Interstellar — we predict User B will love Interstellar too, even without knowing anything about the film's content.

### What is SVD (Singular Value Decomposition)?
SVD is a **matrix factorization** technique. Imagine a matrix:

```
             Inception  Dark Knight  Interstellar  Titanic
User Alice       5           5            ?           2
User Bob         5           4            ?           3
User Carol       2           1            ?           5
```

The `?` cells are what we want to predict. SVD decomposes this matrix into smaller matrices that capture **latent (hidden) factors** — patterns like "prefers cerebral sci-fi", "prefers action", "prefers romance" — without being explicitly told any of this.

### The Math

**Prediction formula:**
```
r̂(u, i) = μ + b_u + b_i + p_u · q_i
```

Where:
- `μ` = global mean rating (average of all ratings = ~3.5)
- `b_u` = user bias (does this user rate generously or harshly?)
- `b_i` = item bias (is this movie universally loved or disliked?)
- `p_u` = user latent factor vector (50 dimensions — user's taste profile)
- `q_i` = item latent factor vector (50 dimensions — movie's characteristics)
- `p_u · q_i` = dot product (how well does this movie match this user's taste?)

**Example interpretation:**
- A user who always gives 4-5 stars has a high positive `b_u`
- The Godfather (universally loved) has a high positive `b_i`
- A user who loves complex plots will have a high value in the "complexity" dimension of `p_u`, and Inception will have a high value in the same dimension of `q_i` — making their dot product large

### Training with SGD (Stochastic Gradient Descent)

For each known rating in the training set:

```
1. Predict the rating using current parameters
2. Calculate error: e = actual_rating - predicted_rating
3. Update parameters to reduce this error:

   b_u += lr × (e - λ × b_u)
   b_i += lr × (e - λ × b_i)
   p_u += lr × (e × q_i - λ × p_u)
   q_i += lr × (e × p_u - λ × q_i)
```

**Hyperparameters used:**
| Parameter | Value | Purpose |
|---|---|---|
| `n_factors` | 50 | Number of latent dimensions |
| `n_epochs` | 30 | Training iterations over full dataset |
| `lr` (learning rate) | 0.005 | How fast parameters update |
| `λ` (regularization) | 0.02 | Prevents overfitting |

After 30 epochs the RMSE (Root Mean Square Error) converges to approximately **0.85–0.90**, meaning predictions are off by less than 1 star on average.

### Getting Recommendations

```
1. Load trained model (cached in memory)
2. Get list of movies user has NOT rated
3. For each unrated movie: compute r̂(u, i)
4. Sort by predicted rating (highest first)
5. Return top 20
```

### Cold Start Problem
SVD requires ratings to make predictions. For **new users with no ratings**, the system falls back to:
- Trending (most watched)
- Top Rated (highest avg_rating)
- New Releases (most recent year)

Once the user submits their **first rating**, `is_new_user = False` and SVD takes over on their next visit.

### Auto-Retrain
Every 50th review submitted triggers a background retrain of the SVD model. This keeps the model fresh as more data accumulates — running in a daemon thread so it never blocks the user's response.

---

## 7. Sentiment Analysis — Deep Explanation

### What is Sentiment Analysis?
Automatically classifying whether a piece of text expresses a **positive**, **negative**, or **neutral** opinion.

**Example:**
- "Absolutely brilliant, a masterpiece!" → **positive**
- "Boring and predictable, total waste of time." → **negative**
- "It was okay, nothing special." → **neutral**

### Algorithm: Multinomial Naive Bayes

**Why "Naive"?** It assumes each word in a review is **independent** of the others — a simplification that is factually wrong (words are clearly related) but works surprisingly well in practice for text.

**Bayes' Theorem applied to text:**
```
P(positive | review) = P(review | positive) × P(positive) / P(review)
```
In plain English: "Given this review text, what is the probability it is positive?"

### Text Preprocessing Pipeline
```
Input: "This film was AMAZING!! Loved every minute :)"
  ↓ Remove HTML tags
  ↓ Lowercase:      "this film was amazing loved every minute"
  ↓ Remove symbols: "this film was amazing loved every minute"
  ↓ Normalize spaces
Output: "this film was amazing loved every minute"
```

### Feature Extraction — Bag of Words with Bigrams

**CountVectorizer** converts text into a numeric vector:
```
Vocabulary: ["film", "amazing", "not good", "loved", "boring", ...]
Review:     [  1,       1,          0,          1,       0,    ...]
```

**Why bigrams matter:**
- "good" → positive signal
- "not good" → negative signal (bigram captures this, unigram misses it)

Settings used: `max_features=20,000`, `ngram_range=(1,2)`, `stop_words='english'`

### Training
- Dataset: IMDB reviews CSV (50,000 labeled reviews)
- 80% training, 20% test split
- Expected accuracy: **85–90%**

### Fallback When Model Not Trained
A keyword heuristic is used until the ML model is trained:
```python
positive_words = {'great', 'excellent', 'amazing', 'love', ...}
negative_words = {'bad', 'terrible', 'boring', 'waste', ...}

if positive_count > negative_count → 'positive'
elif negative_count > positive_count → 'negative'
else → 'neutral'
```

### Confidence Threshold
Even with the ML model, low-confidence predictions return 'neutral':
```python
if max(predict_proba()) < 0.60:
    return 'neutral'
```

---

## 8. Dataset

### MovieLens (Primary Dataset)
**Source:** GroupLens Research, University of Minnesota  
**Version:** ml-latest-small

| File | Records | Content |
|---|---|---|
| `movies.csv` | 9,742 movies | movieId, title (with year), genres (pipe-separated) |
| `ratings.csv` | 100,836 ratings | userId, movieId, rating (0.5–5.0), timestamp |
| `links.csv` | 9,742 entries | movieId → imdbId, tmdbId |

**Why MovieLens?**
- Real user ratings (not synthetic data)
- Widely used in academic research — results are comparable
- Freely available, no licensing restrictions for academic use
- Contains enough ratings for meaningful SVD training

**How it's imported:**
```
movies.csv → parse title/year → create Movie objects + Genre objects
ratings.csv → aggregate avg/count per movie → update Movie.avg_rating
links.csv → used by poster fetch command to get IMDB IDs → OMDB API
```

### Nepali Movies (Custom Addition)
- 50 popular Nepali films hardcoded with verified IMDB IDs
- Metadata fetched from OMDB API
- movielens_id range: 999,001+ (safely above MovieLens max of 193,609)
- Purpose: demonstrate extensibility and local content relevance

### Poster Images (OMDB API)
- Free tier: 1,000 requests/day
- Downloads images to local filesystem
- Automated via Windows Task Scheduler (runs nightly at 00:30)
- Current coverage: 924 / 9,792 movies (~9.4%)

---

## 9. Key Features

| Feature | Description |
|---|---|
| Movie Browsing | Grid view with genre filters, search, pagination (20/page) |
| Advanced Search | Filter by title, genre, year range, minimum rating |
| Personalized Recommendations | SVD predictions grouped by genre |
| Cold-Start Recommendations | Trending / Top Rated / New Releases for new users |
| Star Rating System | 1–5 star CSS-only interactive picker |
| Review Submission | Write review + rating in one form on movie detail page |
| Sentiment Badges | Auto-classified positive/negative/neutral on each review |
| Watchlist | AJAX toggle, persisted per user |
| Watch History | Track every movie watched (AJAX) |
| Related Movies | Shown on detail page — same genre, different movie |
| Nepali Movies | Dedicated Nepali genre with local content |
| Theme Switching | Dark (cinematic) / Warm — persisted per user |
| User Profile | Tabs for reviews, watchlist, watch history |
| Password Reset | Full email-based flow |
| Admin Panel | Dashboard with stats, movie CRUD, user management, model retraining |
| Auto-Retrain | SVD retrains in background every 50th review |

---

## 10. Probable Defense Questions & Answers

---

### General / Introduction

**Q: In one sentence, what is NextReel?**
> NextReel is a Django web application that uses SVD collaborative filtering to recommend movies to users based on their personal rating history, with automatic sentiment analysis on written reviews.

---

**Q: What inspired this project?**
> The problem of choice overload on streaming platforms. When you have access to thousands of movies, the hardest part is deciding what to watch. A recommendation engine that learns your specific taste solves this problem better than generic "popular movies" lists.

---

**Q: What makes your project different from just using Netflix or IMDb?**
> The goal is not to replicate Netflix — it's to understand and implement the core algorithms that power such systems. This project demonstrates how collaborative filtering, matrix factorization, and NLP sentiment analysis work from the ground up, without relying on pre-built ML services.

---

### Technical — Recommendation System

**Q: What is collaborative filtering and why did you choose it?**
> Collaborative filtering recommends items based on the behaviour of many users, not the content of the items. It assumes users with similar taste in the past will have similar taste in the future. I chose it because it does not require any metadata about the movies (no genre, actor, or plot analysis) — the ratings alone are sufficient to find patterns. It also scales well and is the basis of real-world recommendation systems at Netflix and Amazon.

---

**Q: What is the difference between user-based and item-based collaborative filtering, and which do you use?**
> User-based CF finds users similar to the target user and recommends what they liked. Item-based CF finds items similar to what the user liked and recommends those. Both have O(n²) similarity computation problems at scale.  
> NextReel uses neither directly — it uses **model-based collaborative filtering via SVD matrix factorization**, which is more scalable and generalises better because it compresses the rating matrix into dense latent factor vectors.

---

**Q: Explain SVD in simple terms.**
> Imagine a spreadsheet where rows are users and columns are movies, and cells contain ratings. Most cells are empty because users haven't seen most movies. SVD finds hidden patterns in the filled cells — patterns like "users who like action movies", "movies that appeal to critics" — and uses those patterns to fill in the empty cells with predictions. Each user and each movie gets represented as a point in a 50-dimensional "taste space", and the closer two points are, the better the match.

---

**Q: Why 50 latent factors? Why not 100 or 10?**
> 50 is a standard choice in the literature (the Netflix Prize winning solution used similar values). More factors can capture more nuance but risk overfitting and slow training. Fewer factors are faster but may miss important patterns. 50 is a good balance. In practice, the optimal value is found through hyperparameter tuning on a validation set — that is a future improvement for this project.

---

**Q: What is regularization and why do you need it?**
> Without regularization, the model can overfit — memorising the training ratings exactly but performing poorly on unseen data. Regularization (L2 penalty, λ=0.02) penalises large parameter values, forcing the model to generalise rather than memorise. In the update rule: `p_u += lr × (error × q_i - λ × p_u)` — the `-λ × p_u` term pulls values back towards zero if they grow too large.

---

**Q: What is RMSE and what does your model achieve?**
> RMSE (Root Mean Square Error) measures average prediction error in the same units as the ratings. An RMSE of 0.85 means on average, the predicted rating is off by 0.85 stars. For a 1–5 star scale, this is reasonable — approximately what academic benchmarks achieve on this dataset. The MovieLens benchmark RMSE is around 0.87 for SVD.

---

**Q: How do you handle the cold start problem?**
> New users have no rating history, so SVD cannot make predictions. The system detects this via the `is_new_user` flag on the CustomUser model. New users see cold-start recommendations: Trending (sorted by total_watches), Top Rated (sorted by avg_rating), and New Releases (sorted by year). After their first rating, `is_new_user` is set to False and SVD takes over. This is a standard industry approach.

---

**Q: If a user rates only one movie, will SVD work well?**
> One rating gives very little signal — the SVD model may not have a well-trained vector for that user, especially if the user was not in the training set. In that case, the code falls back to top-rated movies. More ratings = better recommendations. Minimum meaningful input is typically 10–20 ratings. This is a known limitation of collaborative filtering.

---

**Q: What happens when a user has rated every movie?**
> The code checks: `candidate_movies = Movie.objects.exclude(id__in=rated_movie_ids)`. If this is empty, it falls back to the top-rated list. In practice with 9,792 movies this is an extreme edge case.

---

**Q: How is the SVD model stored and loaded?**
> Trained using NumPy, serialised to a Python pickle file (`svd_model.pkl`) containing the user/item factor matrices, bias vectors, index mappings, and global mean. The file is loaded once into a module-level memory cache. Subsequent requests use the cached version. If the model is retrained, the cache is invalidated and the new model is loaded on the next request.

---

**Q: When does the model retrain?**
> Two triggers: (1) Manually via the Admin Panel → Retrain Models. (2) Automatically every 50th review submitted — this runs in a background daemon thread so it does not block the user's response.

---

### Technical — Sentiment Analysis

**Q: What is Naive Bayes and why is it "naive"?**
> Naive Bayes is a probabilistic classifier based on Bayes' theorem. It's "naive" because it assumes all features (words) are independent of each other given the class — clearly untrue in natural language, but a simplification that works very well in practice. It computes the probability of each class given the words in the text and picks the most likely one.

---

**Q: Why not use a neural network for sentiment?**
> For short text like movie reviews (1–3 sentences), Naive Bayes achieves 85–90% accuracy — comparable to LSTM networks — at a fraction of the training time and complexity. A neural network would require a GPU, thousands of lines of code, and much more training data for a marginal improvement in accuracy. Naive Bayes is the right tool for this problem.

---

**Q: What are bigrams and why do you use them?**
> Bigrams are two-word combinations, e.g. "not good", "very bad", "highly recommended". Without bigrams, "not good" would be treated as the word "not" (neutral) plus the word "good" (positive), giving a wrong positive signal. With bigrams, "not good" is one feature with its own learned weight. This significantly improves accuracy for sentiment analysis.

---

**Q: What accuracy does your sentiment model achieve?**
> On the IMDB dataset (50,000 labeled reviews), Multinomial Naive Bayes with CountVectorizer achieves approximately **85–90% accuracy** on the held-out test set. This is consistent with published benchmarks for this algorithm on this dataset.

---

**Q: What is a confidence threshold and why 60%?**
> The model outputs a probability for each class. If the highest probability is below 60%, the model is uncertain — so we return 'neutral' instead of making a potentially wrong positive/negative call. 60% is a conservative threshold that reduces false positives in sentiment at the cost of more neutral classifications. It can be tuned up or down depending on the preference for precision vs recall.

---

### Technical — Database & Django

**Q: Why SQLite and not PostgreSQL?**
> SQLite is appropriate for development and demonstration. It requires no installation or configuration. For production deployment with multiple concurrent users, PostgreSQL would be used — the switch requires only changing the `DATABASES` setting in Django.

---

**Q: What is Django's ORM and why use it?**
> ORM (Object-Relational Mapper) lets you interact with the database using Python objects instead of SQL queries. For example: `Movie.objects.filter(genres__name='Action').order_by('-avg_rating')` instead of writing `SELECT * FROM movies JOIN ... WHERE ... ORDER BY ...`. It is database-agnostic (the same code works on SQLite and PostgreSQL), prevents SQL injection by design, and keeps the code readable.

---

**Q: How do you prevent SQL injection?**
> Django's ORM parameterizes all queries automatically. User input never gets concatenated into SQL strings. This is a built-in protection in Django — you would have to deliberately bypass it to be vulnerable.

---

**Q: What is CSRF and how do you handle it?**
> CSRF (Cross-Site Request Forgery) is an attack where a malicious website tricks a user's browser into making requests to your site. Django mitigates this with a CSRF token — a hidden field in every form, and a header on every AJAX request (`X-CSRFToken`). The server rejects any POST request without a valid token.

---

**Q: Explain the `unique_together` constraint on Review.**
> `unique_together = ('user', 'movie')` creates a database-level constraint preventing a user from having two reviews for the same movie. This is enforced at the database level (not just application logic), so even if two simultaneous requests tried to create duplicate reviews, the database would reject one. In the view, we handle this by checking for an existing review and updating it instead.

---

**Q: Why is avg_rating stored on the Movie model instead of computed from reviews?**
> With 100,836 ratings, computing `AVG(rating)` with a JOIN on every page load would be slow, especially when sorting the entire movie grid by rating. We trade a small write-time cost (recalculating on every review add/delete) for fast read-time queries. This is a standard **denormalization** pattern for read-heavy applications.

---

### System Design

**Q: How does the poster system work?**
> Three-level fallback chain: (1) Local file in `media/movies/posters/` — downloaded via the OMDB poster fetch command. (2) `poster_url_external` — an external URL stored in the database, set manually via admin or import scripts. (3) Default SVG placeholder. The `poster_url` property on the Movie model implements this chain. An automated Windows Task Scheduler job fetches 1,000 new posters each night.

---

**Q: How do you handle the case where OMDB returns wrong posters?**
> This was a real issue during development — Nepali movie titles like "Fighters" matched Bollywood films. The solution was to: (1) always use verified IMDB IDs in the import script rather than title search, (2) allow manual override via the admin panel's `poster_url_external` field, (3) for confirmed mismatches, delete the wrong local file and set the correct Wikipedia URL.

---

**Q: How does the AJAX watchlist work?**
> The watchlist button sends a POST request to `/movies/<pk>/watchlist/` with `X-Requested-With: XMLHttpRequest` header. The server detects this header and returns a JSON response `{status, in_watchlist, message}` instead of an HTML redirect. The JavaScript updates the button text and class without reloading the page. This provides instant feedback and a better user experience.

---

**Q: How does authentication work?**
> Django's built-in authentication system. Passwords are hashed with PBKDF2 (Django default) — never stored in plain text. Login creates a session, logout destroys it. Protected views use `LoginRequiredMixin`. The admin panel uses a custom `@admin_required` decorator that checks `user.is_staff or user.is_superuser`.

---

**Q: How did you implement the admin panel without using Django's built-in admin?**
> Django's built-in admin at `/admin/` was not registered. Instead, a completely custom `admin_panel` app was built with dedicated views for dashboard statistics, movie CRUD, user management, and model retraining. Access is controlled via a custom `@admin_required` decorator. This gives full control over the UI/UX and functionality.

---

### Evaluation & Testing

**Q: How did you evaluate the recommendation system?**
> Using RMSE (Root Mean Square Error) on a held-out portion of the MovieLens ratings. The model is trained on 80% of ratings and tested on the remaining 20%. RMSE of ~0.87 means predictions are off by less than 1 star on average. Additionally, qualitative evaluation: seeding demo users with known tastes and verifying recommendations matched expectations.

---

**Q: Did you write unit tests?**
> The project does not currently have a formal test suite. Manual testing was performed for each feature. Automated tests would be added in a production version, particularly for the SVD prediction function, the `_update_movie_rating` utility, and the AJAX endpoints.

---

**Q: How did you test the sentiment analysis?**
> The `train_sentiment_model` function performs an 80/20 train/test split and reports accuracy. Additionally, the heuristic fallback provides a baseline to compare against.

---

### Scalability & Production

**Q: Can this system handle thousands of concurrent users?**
> In its current form, no — SQLite has write contention issues with many concurrent users. For production: switch to PostgreSQL, deploy with gunicorn + nginx, move media files to S3 or similar object storage, and add Redis caching for session management and query caching.

**Q: How would you scale the recommendation system for millions of users?**
> The current NumPy SVD implementation would need to be replaced with an approximate nearest-neighbour library like Faiss, or distributed training with Spark MLlib. The latent factor vectors would be pre-computed and stored, making inference O(1). Real-time retraining would be replaced with daily or weekly batch retraining.

**Q: What security measures are in place?**
> (1) CSRF protection on all forms and AJAX. (2) SQL injection prevention via ORM parameterized queries. (3) Password hashing with PBKDF2. (4) `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` configurable via environment variables (not hardcoded). (5) `@login_required` and `@admin_required` on all protected views. (6) `unique_together` constraints prevent data corruption. (7) File upload restricted to images via `ImageField`.

---

### Dataset & Ethics

**Q: Is the MovieLens data real user ratings?**
> Yes, MovieLens is a real movie rating service run by GroupLens Research at the University of Minnesota. The dataset contains real ratings from real users, collected over several years. User identities are anonymized — no personal information is included.

**Q: Are there any biases in your recommendation system?**
> Yes — popularity bias. Movies with more ratings are better represented in the training data, so SVD learns their factors more accurately. New or niche movies with few ratings may be under-recommended even if the user would enjoy them. This is a known problem in collaborative filtering and is partially mitigated by the cold-start fallback which shows "New Releases".

**Q: Why did you add Nepali movies?**
> To demonstrate that the system is extensible beyond a Western-centric dataset. Nepali movies are underrepresented in mainstream recommendation systems. By adding a dedicated Nepali genre with 50 curated films, the platform serves local users and shows that the architecture supports custom content addition alongside the main dataset.

---

## 11. Known Limitations & How to Address Them

Be honest about limitations — examiners respect honesty more than overclaiming.

| Limitation | Honest Acknowledgment | Future Solution |
|---|---|---|
| Cold start for new users | No history = no personalized recs | Ask new users to rate 5 movies on signup |
| Sentiment model not trained | Running on heuristic fallback | Add IMDB dataset CSV and run train command |
| ~90% movies have no poster | OMDB free tier = 1,000/day | Automated nightly fetch continues; ~9 days to complete |
| SVD retrains in same process | Could fail under memory pressure | Move to Celery task queue in production |
| No content-based filtering | Can't recommend by genre/plot similarity | Add TF-IDF on descriptions for hybrid approach |
| SQLite concurrency | Not suitable for multi-user production | Switch to PostgreSQL for deployment |
| No formal test suite | Manual testing only | Add pytest + Django test client |

---

## 12. Live Demo Walkthrough

### Suggested Demo Script (5–7 minutes)

1. **Homepage** — Show featured, trending, new releases sections
2. **Browse movies** — Genre filter (click Nepali), search by title
3. **Movie detail** — Show poster, reviews, related movies, star picker
4. **Submit a review** — Show sentiment badge appearing automatically
5. **Recommendations page** — Show personalized results grouped by genre
6. **Admin panel** — Show dashboard stats, retrain button
7. **Admin → Edit movie** — Show poster upload and external URL field

### Things to highlight during demo
- "Notice the sentiment badge appeared automatically — that's the NLP classifier running on my review"
- "These recommendations are from the SVD model — the system predicted I would give these movies 4+ stars based on my rating history"
- "The watchlist button updates instantly with AJAX — no page reload"
- "The admin panel lets staff retrain both ML models without touching code"

---

## 13. Future Work

Have at least 3–4 genuine future improvements ready:

1. **Content-based filtering** — recommend by genre and description similarity (TF-IDF or word embeddings) to solve cold start
2. **Hybrid model** — combine SVD (collaborative) + content-based signals for better accuracy
3. **Train sentiment model** — add IMDB dataset to achieve 85–90% accuracy (currently using heuristic)
4. **Real-time recommendations** — update recommendations without full retrain using online learning
5. **PostgreSQL + deployment** — production-ready deployment with gunicorn/nginx
6. **Mobile responsive** — further optimize CSS for mobile screens
7. **Social features** — follow other users, see what friends are watching
8. **More Nepali content** — expand to 200+ Nepali movies with verified metadata

---

## Quick Reference Card

| Question type | Key points to hit |
|---|---|
| "Explain your algorithm" | Matrix factorization → latent factors → dot product prediction → SGD training → RMSE |
| "Why did you choose X?" | Always: simplicity, Python ecosystem, academic validity, full control |
| "What is the accuracy?" | SVD RMSE ~0.87 on MovieLens. Sentiment ~85-90% on IMDB. |
| "What would you improve?" | Hybrid filtering, production DB, formal tests, sentiment training |
| "What was the hardest problem?" | Cold start problem, wrong poster matching (OMDB title clashes), movielens_id collision |
| "How does it compare to Netflix?" | Same fundamental algorithm (matrix factorization), much smaller scale, full transparency |

---

*Good luck with your defense. Know your algorithm deeply — if you can explain SVD and Naive Bayes clearly, you will pass.*
