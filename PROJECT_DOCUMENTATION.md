# NextReel: Movie Recommendation System

**Final Semester Project**
Bachelor of Science in Computer Science / Information Technology

**Submitted by:** Manoj
**Academic Year:** 2025–2026
**Project Repository:** NextReel
**Technology Stack:** Django 4.2, Python 3.14, SQLite, SVD Collaborative Filtering, Naive Bayes Sentiment Analysis

---

## Table of Contents

1. [Abstract](#abstract)
2. [Chapter 1: Introduction](#chapter-1-introduction)
   - 1.1 Background
   - 1.2 Problem Statement
   - 1.3 Objectives
   - 1.4 Scope
   - 1.5 Limitations
3. [Chapter 2: Literature Review](#chapter-2-literature-review)
   - 2.1 Collaborative Filtering
   - 2.2 Content-Based Filtering
   - 2.3 Hybrid Recommender Systems
   - 2.4 Sentiment Analysis in Recommender Systems
4. [Chapter 3: System Requirements](#chapter-3-system-requirements)
   - 3.1 Functional Requirements
   - 3.2 Non-Functional Requirements
   - 3.3 Hardware Requirements
   - 3.4 Software Requirements
5. [Chapter 4: System Design](#chapter-4-system-design)
   - 4.1 Architecture Overview
   - 4.2 MVC/MVT Pattern in Django
   - 4.3 Database Entity-Relationship Description
   - 4.4 Data Flow Description
6. [Chapter 5: Technology Stack](#chapter-5-technology-stack)
7. [Chapter 6: Implementation](#chapter-6-implementation)
   - 6.1 User Authentication Module
   - 6.2 Movie Browsing Module
   - 6.3 Search and Filtering Module
   - 6.4 Review System Module
   - 6.5 Recommendation Engine Module
   - 6.6 Watchlist and Watch History Module
   - 6.7 Admin Panel Module
8. [Chapter 7: Machine Learning Components](#chapter-7-machine-learning-components)
   - 7.1 SVD Collaborative Filtering
   - 7.2 Naive Bayes Sentiment Analysis with TF-IDF
   - 7.3 Training Process
   - 7.4 Model Evaluation
   - 7.5 Cold-Start Problem and Fallback Strategy
9. [Chapter 8: Testing](#chapter-8-testing)
   - 8.1 Types of Testing
   - 8.2 Functional Test Cases
   - 8.3 Edge Cases and Boundary Testing
10. [Chapter 9: Results and UI Description](#chapter-9-results-and-ui-description)
    - 9.1 Home Page
    - 9.2 Movie Browse and Search Pages
    - 9.3 Movie Detail Page
    - 9.4 Recommendations Page
    - 9.5 User Profile Page
    - 9.6 Admin Panel
11. [Chapter 10: Conclusion and Future Work](#chapter-10-conclusion-and-future-work)
    - 10.1 Conclusion
    - 10.2 Future Work
12. [References](#references)
13. [Defense Q&A Section](#defense-qa-section)

---

## Abstract

NextReel is a full-stack web-based movie recommendation system developed as a final semester project using the Django web framework. The system integrates machine learning techniques to deliver personalized movie recommendations and automated sentiment classification of user reviews. The recommendation engine is built on Singular Value Decomposition (SVD) collaborative filtering, which learns latent user and item factors from historical rating data using stochastic gradient descent (SGD) optimization. For new users who have not yet submitted any ratings, a cold-start strategy presents curated lists of trending, top-rated, and newly released movies.

Review text submitted by users is automatically analyzed using a Naive Bayes classifier trained on the IMDB 50K movie review dataset, with TF-IDF feature extraction via a CountVectorizer. The classifier achieves approximately 70–85% accuracy on held-out test data.

The platform includes full user account management, movie browsing with pagination and advanced filtering, a personal watchlist, watch history tracking, and a custom administrative dashboard for managing users, movies, and ML model retraining. The frontend employs two distinct visual themes — Cinematic Dark and Warm Glow — built entirely in custom CSS with no external UI frameworks. The MovieLens dataset serves as the primary data source, imported via a custom Django management command.

NextReel demonstrates the practical integration of machine learning into a production-grade web application, addressing real-world challenges such as the cold-start problem, model persistence, and graceful degradation when models are unavailable.

---

## Chapter 1: Introduction

### 1.1 Background

The exponential growth of digital content has created an information overload problem for consumers. The global film industry produces thousands of movies annually, and streaming platforms catalog tens of thousands of titles. Without effective discovery tools, users spend significant time searching for content rather than consuming it, leading to decision fatigue and reduced engagement.

Recommender systems have emerged as a critical technology in addressing this problem. Platforms such as Netflix, Amazon Prime Video, and Spotify rely heavily on recommendation algorithms to surface relevant content, driving substantial increases in user engagement and platform retention. Netflix has publicly stated that its recommendation system saves approximately one billion dollars per year by reducing subscriber churn [1].

Academic research on recommender systems has accelerated since the Netflix Prize competition (2006–2009), which drew widespread attention to collaborative filtering techniques and produced significant algorithmic advances. The winning solution, an ensemble of matrix factorization methods, established SVD-based approaches as a gold standard for rating prediction tasks [2].

NextReel is built upon these foundations, applying SVD collaborative filtering in a practical Django web application to serve personalized movie recommendations to registered users.

### 1.2 Problem Statement

While large-scale recommender systems exist on commercial platforms, building such a system from scratch as an integrated full-stack application involves several technical challenges:

1. **Cold-start problem:** New users have no rating history, making personalized recommendations impossible initially.
2. **Model persistence and integration:** Trained ML models must be serialized, stored, and seamlessly loaded within a web application context without degrading response times.
3. **Data sparsity:** User-movie rating matrices are typically very sparse (most users rate only a tiny fraction of available movies), making accurate factor decomposition challenging.
4. **Automatic model maintenance:** As new ratings arrive, the model becomes stale. Deciding when and how to retrain without disrupting live users requires careful design.
5. **Qualitative feedback integration:** Star ratings alone provide limited signal. Review text contains richer sentiment information that can complement quantitative ratings.

NextReel addresses each of these challenges through its architecture and fallback mechanisms.

### 1.3 Objectives

The primary objectives of this project are:

1. To design and implement a full-stack web application for movie discovery using the Django framework.
2. To implement a collaborative filtering recommendation engine using SVD matrix factorization with SGD optimization.
3. To implement an automatic sentiment analysis module using Naive Bayes classification and TF-IDF feature extraction.
4. To handle the cold-start problem with a curated fallback recommendation strategy.
5. To implement automatic model retraining triggered by accumulated new review data.
6. To build a custom administrative interface for managing users, movies, and ML models without requiring command-line access.
7. To provide a polished, responsive user interface with theme customization.
8. To demonstrate graceful degradation when ML models are unavailable.

### 1.4 Scope

The project scope encompasses the following:

- A complete web application with user registration, authentication, and profile management.
- A movie catalog imported from the MovieLens dataset (up to 9,742+ movies with ratings).
- A personalized recommendation system for authenticated users with rating history.
- A cold-start recommendation strategy for new or unauthenticated users.
- Automatic sentiment classification of review text.
- A custom administrative dashboard for system management.
- Two frontend themes with persistent preference storage.
- A data import pipeline for MovieLens CSV datasets.
- ML model training and retraining workflows, both automated and manual.

The project is scoped as a single-server application suitable for academic demonstration. It does not include features such as social networking, real-time notifications, mobile applications, or distributed deployment.

### 1.5 Limitations

The following limitations are acknowledged:

1. **SQLite database:** SQLite is not designed for high-concurrency production environments. It is suitable for development and academic demonstration but would need to be replaced with PostgreSQL or MySQL for a production deployment serving many concurrent users.
2. **No external APIs:** The system does not integrate with external movie databases (e.g., TMDB, OMDB) for poster images, trailers, or additional metadata. Posters must be uploaded manually or are absent (showing a default SVG).
3. **SVD scalability:** The custom NumPy/Pandas SVD implementation iterates over all ratings in Python loops, which becomes slow for very large datasets (millions of ratings). Libraries such as Surprise or implicit would be more efficient at scale.
4. **Sentiment accuracy:** The Naive Bayes classifier achieves 70–85% accuracy. Sarcasm, mixed sentiments, and very short reviews are frequently misclassified. A transformer-based model (e.g., BERT) would achieve higher accuracy but would significantly increase complexity and resource requirements.
5. **Single-language support:** The sentiment model is trained on English-language reviews only. Non-English review text will be classified unreliably.
6. **No real-time recommendations:** Recommendations are computed on demand at page load time. For large user-movie matrices, this could introduce latency. Pre-computation and caching would be required at scale.

---

## Chapter 2: Literature Review

### 2.1 Collaborative Filtering

Collaborative filtering (CF) is the most widely deployed approach to recommendation, operating on the principle that users who agreed in the past will agree in the future. CF can be divided into two broad families: memory-based (neighborhood methods) and model-based (latent factor models).

**Memory-based CF** computes similarity between users (user-based CF) or items (item-based CF) directly from the rating matrix. User-based CF recommends items liked by similar users; item-based CF recommends items similar to those a user has already rated. While conceptually simple, memory-based CF scales poorly with large datasets due to the O(n²) cost of pairwise similarity computation.

**Model-based CF** uses the rating matrix to learn a compact representation of users and items. Matrix factorization methods, particularly SVD and its variants (ALS, BPR), have dominated the literature since Koren et al. [3] demonstrated their effectiveness in the Netflix Prize. These methods decompose the rating matrix R ≈ UVᵀ, where U contains user latent factors and V contains item latent factors. Predictions for unobserved ratings are made by the dot product of the corresponding row vectors.

The **FunkSVD** algorithm, introduced by Simon Funk during the Netflix Prize, demonstrated that explicit SVD decomposition is unnecessary; instead, SGD can directly optimize U and V to minimize prediction error on observed ratings, which is far more tractable for sparse matrices [4].

### 2.2 Content-Based Filtering

Content-based filtering (CBF) recommends items similar in attribute to those a user has previously liked. In the movie domain, item attributes include genre, director, cast, keywords, and plot descriptions. Similarity is typically measured using TF-IDF vector representations and cosine similarity.

CBF has several advantages: it does not require data from other users (no cold-start for items), and it can recommend niche items that have not been rated by many users. However, it is limited by feature availability and quality, and tends to over-specialize (recommending items too similar to past choices), reducing serendipity.

NextReel implements a lightweight form of CBF in its "Related Movies" feature, which identifies movies sharing genres with the currently viewed movie using Django's ORM rather than a dedicated vector similarity computation.

### 2.3 Hybrid Recommender Systems

Hybrid systems combine collaborative and content-based approaches to leverage the strengths of each while mitigating their weaknesses. Burke [5] categorizes hybrid methods into weighted, switching, mixed, feature combination, cascade, feature augmentation, and meta-level hybrids.

Netflix's production system is a sophisticated hybrid that combines dozens of individual models [6]. For academic projects, simpler hybrids are more tractable. NextReel's cold-start fallback (curated lists based on aggregate statistics) can be viewed as a lightweight hybrid: the system switches from personalized CF recommendations to popularity-based recommendations for new users.

### 2.4 Sentiment Analysis in Recommender Systems

Sentiment analysis (opinion mining) is the computational study of opinions, sentiments, and emotions expressed in text [7]. In the context of recommender systems, review text provides a richer signal than star ratings alone. A user who writes "the cinematography was stunning but the plot was predictable" conveys nuanced information that a 3-star rating cannot capture.

**Naive Bayes classifiers** are a well-established baseline for text classification. They apply Bayes' theorem under the "naive" independence assumption: each word is treated as independent of all others given the class label. Despite this strong assumption, Naive Bayes classifiers perform surprisingly well on document classification tasks, particularly with sufficient training data [8].

**TF-IDF (Term Frequency-Inverse Document Frequency)** is a standard text representation technique. CountVectorizer (as used in NextReel) captures term frequency counts without the IDF weighting, which is appropriate for Naive Bayes since the model learns the discriminative weight of each term through its conditional probabilities.

Pang and Lee [9] demonstrated that sentiment classification of movie reviews achieves around 80–86% accuracy using machine learning approaches, which aligns with the performance observed in NextReel's sentiment module.

---

## Chapter 3: System Requirements

### 3.1 Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Users shall be able to register with a username, email, and password. |
| FR-02 | Users shall be able to log in and log out securely. |
| FR-03 | Users shall be able to view and edit their profile (bio, avatar, theme preference). |
| FR-04 | Users shall be able to browse the complete movie catalog in paginated form (20 per page). |
| FR-05 | Users shall be able to search movies by title (word-matching), genre, year range, and minimum rating. |
| FR-06 | Users shall be able to view a movie detail page with description, genres, reviews, and related movies. |
| FR-07 | Authenticated users shall be able to submit a star rating (1–5) and text review for any movie. |
| FR-08 | Each submitted review shall be automatically classified as positive, negative, or neutral. |
| FR-09 | Authenticated users shall be able to add and remove movies from their personal watchlist. |
| FR-10 | Authenticated users shall be able to mark movies as watched, recording a timestamped history entry. |
| FR-11 | The system shall generate personalized movie recommendations for users with at least one review. |
| FR-12 | New or unauthenticated users shall receive cold-start recommendations (trending, top-rated, new). |
| FR-13 | Staff users shall be able to access a custom admin dashboard. |
| FR-14 | Staff users shall be able to activate/deactivate user accounts and grant/revoke staff privileges. |
| FR-15 | Staff users shall be able to add, edit, and delete movies. |
| FR-16 | Staff users shall be able to trigger retraining of SVD and sentiment ML models. |
| FR-17 | The system shall automatically retrain the SVD model every 50 new reviews. |
| FR-18 | The system shall import movies and ratings from MovieLens CSV files via a management command. |

### 3.2 Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-01 | **Usability:** The interface shall be intuitive and require no prior technical knowledge. |
| NFR-02 | **Performance:** All standard page loads (browse, search, detail) shall complete within 3 seconds on localhost. |
| NFR-03 | **Security:** Passwords shall be hashed using Django's default PBKDF2 algorithm. CSRF protection shall be active on all forms. |
| NFR-04 | **Reliability:** If any ML model is unavailable, the system shall degrade gracefully with fallback behavior. |
| NFR-05 | **Maintainability:** Code shall be organized into discrete Django apps with single-responsibility models, views, and URLs. |
| NFR-06 | **Portability:** The application shall run on any OS supporting Python 3.14 (Windows, Linux, macOS). |
| NFR-07 | **Scalability (academic):** The architecture shall support future migration to a production database without major refactoring. |
| NFR-08 | **Accessibility:** The two UI themes shall provide sufficient color contrast for basic readability. |

### 3.3 Hardware Requirements

**Minimum (Development):**
- CPU: Dual-core processor, 1.5 GHz or higher.
- RAM: 4 GB (8 GB recommended for training ML models on large datasets).
- Storage: 2 GB free disk space (additional space required for the MovieLens dataset and media uploads).

**Recommended (Academic Demo):**
- CPU: Quad-core processor, 2.5 GHz or higher.
- RAM: 8 GB.
- Storage: 10 GB free disk space.

### 3.4 Software Requirements

| Component | Version / Details |
|---|---|
| Operating System | Windows 10/11, Ubuntu 20.04+, or macOS 12+ |
| Python | 3.14 |
| Django | 4.2.x |
| NumPy | Latest stable |
| Pandas | Latest stable |
| scikit-learn | Latest stable (for Naive Bayes, CountVectorizer, train_test_split) |
| Pillow | Latest stable (for image handling) |
| SQLite | Bundled with Python |
| Web Browser | Chrome 90+, Firefox 88+, Edge 90+, Safari 14+ |

All Python dependencies are listed in `requirements.txt` and can be installed with:

```bash
pip install -r requirements.txt
```

---

## Chapter 4: System Design

### 4.1 Architecture Overview

NextReel follows a three-tier web application architecture:

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                    │
│  HTML Templates (Jinja2-style Django Templates)         │
│  Custom CSS (Cinematic Dark / Warm Glow Themes)         │
│  Vanilla JavaScript (AJAX for watchlist/theme toggle)   │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP Request / Response
┌───────────────────────▼─────────────────────────────────┐
│                  APPLICATION LAYER                      │
│  Django Views (Class-Based Views)                       │
│  URL Router (movie_project/urls.py)                     │
│  Django Apps: users, movies, reviews, recommendations,  │
│               admin_panel                               │
│  ML Modules: engine.py (SVD), sentiment.py (NB+TF-IDF) │
└───────────────────────┬─────────────────────────────────┘
                        │ ORM Queries
┌───────────────────────▼─────────────────────────────────┐
│                    DATA LAYER                           │
│  SQLite Database (db.sqlite3)                           │
│  ML Model Files (.pkl): svd_model.pkl, sentiment_model  │
│  Media Files: avatars/, movies/posters/                 │
│  Static Files: css/, js/, images/                       │
└─────────────────────────────────────────────────────────┘
```

### 4.2 MVC/MVT Pattern in Django

Django follows the **Model-View-Template (MVT)** pattern, which is a variant of the classical Model-View-Controller (MVC) pattern:

| MVT Component | Django Element | Role |
|---|---|---|
| **Model** | `models.py` in each app | Defines database schema, relationships, and business logic methods. |
| **View** | `views.py` in each app | Handles HTTP request processing, queries the database via ORM, selects the template, and passes context data. |
| **Template** | `templates/` directory | Renders HTML using Django's template language. Receives context variables from the View. |

The **URL Dispatcher** (`urls.py`) routes incoming HTTP requests to the appropriate View based on URL patterns. This corresponds to the Controller in classical MVC.

**App Boundaries:**

```
movie_project/       ← Project configuration (settings, root URLs, WSGI/ASGI)
users/               ← CustomUser model, registration, login, profile, theme
movies/              ← Movie, Genre, Watchlist, WatchHistory models; browse, search, detail
reviews/             ← Review model, sentiment analysis, review CRUD
recommendations/     ← SVD engine, recommendations view, train_svd command
admin_panel/         ← Custom admin views, decorators
```

### 4.3 Database Entity-Relationship Description

The database schema consists of the following entities and their relationships:

**Entities:**

1. **CustomUser** (extends Django AbstractUser)
   - Fields: id (PK), username, email, password, first_name, last_name, bio, avatar, theme_preference, is_new_user, is_active, is_staff, is_superuser, date_joined.

2. **Genre**
   - Fields: id (PK), name (unique).

3. **Movie**
   - Fields: id (PK), title, year, description, poster, movielens_id (unique), avg_rating, total_ratings, total_watches.

4. **Watchlist**
   - Fields: id (PK), user (FK → CustomUser), movie (FK → Movie), added_at.
   - Constraint: unique_together(user, movie).

5. **WatchHistory**
   - Fields: id (PK), user (FK → CustomUser), movie (FK → Movie), watched_at.

6. **Review**
   - Fields: id (PK), user (FK → CustomUser), movie (FK → Movie), rating (1–5), review_text, sentiment, created_at.
   - Constraint: unique_together(user, movie).

**Relationships:**

```
CustomUser (1) ──────────────── (M) Review
CustomUser (1) ──────────────── (M) Watchlist
CustomUser (1) ──────────────── (M) WatchHistory

Movie (1) ───────────────────── (M) Review
Movie (1) ───────────────────── (M) Watchlist
Movie (1) ───────────────────── (M) WatchHistory

Movie (M) ────────────────── (M) Genre
           [movie_genres junction table]
```

All foreign key relationships use `CASCADE` deletion: deleting a User removes all their reviews, watchlist entries, and watch history. Deleting a Movie similarly removes all associated records.

### 4.4 Data Flow Description

**User Registration and Login Flow:**
1. User submits registration form → `RegisterView` validates form → creates `CustomUser` → logs in → redirect to home.
2. User submits login form → `LoginView` authenticates credentials → creates session → redirect.

**Movie Browse and Search Flow:**
1. HTTP GET request to `/movies/` or `/movies/search/` with query parameters.
2. `MovieListView` / `SearchView` builds Django ORM query with `Q()` objects for multi-word title matching and filter parameters.
3. Results paginated with Django's `Paginator` (20 per page).
4. Template renders movie cards with poster, title, rating.

**Review Submission Flow:**
1. User submits review form (POST) → `AddReviewView`.
2. Form validated; if valid, `analyze_sentiment()` is called on review text.
3. Sentiment analysis: load model from `.pkl` → preprocess text → `vectorizer.transform()` → `model.predict()` → confidence check → return label.
4. Review saved to database; `_update_movie_rating()` recalculates `avg_rating` and `total_ratings` for the movie.
5. If `user.is_new_user`, set to False.
6. Check if total review count is a multiple of 50; if so, trigger `train_svd_model()` asynchronously (non-blocking try/except).

**Recommendation Generation Flow:**
1. User visits `/recommendations/` → `RecommendationView`.
2. If `user.is_new_user` or unauthenticated → return cold-start lists (trending, top-rated, new releases).
3. Otherwise → `get_recommendations(user_id, n=20)`:
   a. Load SVD model from `.pkl` file.
   b. Check if user exists in `user_index` map.
   c. Retrieve set of movie IDs the user has already rated.
   d. For each unrated candidate movie, compute predicted rating: `global_mean + u_bias + i_bias + dot(u_vec, i_vec)`.
   e. Sort by predicted rating descending; return top 20 movies.
4. Group movies by primary genre; pick top 4 most-populated genre groups.
5. Render grouped recommendations template.

---

## Chapter 5: Technology Stack

### Django 4.2 (Backend Web Framework)

Django was selected as the backend framework for its "batteries-included" philosophy, which provides an ORM, authentication system, form validation, CSRF protection, an admin interface, and a URL dispatcher out of the box. This significantly reduces boilerplate code for a full-stack web application.

Django's **Class-Based Views (CBVs)** promote code reuse through inheritance and mixins (e.g., `LoginRequiredMixin` for protecting views). The **ORM** abstracts database interactions, enabling rapid development and making a future database migration (SQLite → PostgreSQL) straightforward by changing only the `DATABASES` setting.

Django 4.2 is a **Long-Term Support (LTS)** release, ensuring security patches and stability.

### Python 3.14 (Programming Language)

Python was chosen for its dominant position in the data science and machine learning ecosystem. The same language is used for both web application logic and ML model training, eliminating the need for polyglot architecture. Python's NumPy and scikit-learn libraries provide highly optimized implementations of the mathematical operations required for SVD and Naive Bayes.

### SQLite (Database)

SQLite is the default database for Django development and is appropriate for academic projects and single-user or low-traffic deployments. Its serverless, file-based architecture requires zero configuration and no separate database process, simplifying setup and portability. The database is stored in a single file (`db.sqlite3`), which makes backups trivial.

For a production deployment with multiple concurrent users, migrating to PostgreSQL would be straightforward given Django's database abstraction layer.

### NumPy and Pandas (Numerical Computing and Data Processing)

NumPy provides the n-dimensional array data structures and linear algebra operations required for the SVD implementation (dot products, array arithmetic, random initialization). Pandas is used for loading and processing the MovieLens CSV files during import and for constructing the ratings DataFrame used in SVD training. Together, they provide a performant, Pythonic environment for numerical ML without requiring specialized libraries.

### scikit-learn (Machine Learning)

scikit-learn provides the `MultinomialNB` (Naive Bayes classifier), `CountVectorizer` (TF-IDF feature extraction), `train_test_split` (data splitting), and `accuracy_score` (evaluation) used in the sentiment analysis module. scikit-learn's consistent API (`fit`, `transform`, `predict`) and excellent documentation made it the natural choice for the NLP pipeline.

### Custom CSS with Two Themes (Frontend Styling)

Rather than using a CSS framework such as Bootstrap or Tailwind CSS, NextReel uses entirely custom CSS. This decision provides full control over the visual design and avoids the generic appearance of framework-based UIs. The Cinematic Dark theme uses deep black backgrounds with gold accents and subtle gradients to evoke a cinema aesthetic. The Warm Glow theme uses amber, cream, and brown tones for a softer, warmer look. Both themes are implemented as CSS custom property sets (`--color-*` variables) that are toggled by a class on the `<body>` element.

### Vanilla JavaScript (Frontend Interactivity)

Minimal JavaScript is used for AJAX interactions (watchlist toggle, theme switching). No JavaScript framework (React, Vue, etc.) was used, keeping the frontend simple and reducing the complexity of the build process. Django's server-rendered templates handle the majority of the UI logic.

### MovieLens Dataset (Training Data)

The MovieLens dataset, maintained by the GroupLens Research group at the University of Minnesota, is a well-established benchmark dataset for recommender systems research [10]. It provides structured, clean movie and rating data that is ideal for bootstrapping the recommendation engine. The small dataset (ml-latest-small) contains 9,742 movies and 100,836 ratings; the full dataset (ml-25m) contains 62,000 movies and 25 million ratings.

---

## Chapter 6: Implementation

### 6.1 User Authentication Module

The authentication module is implemented in the `users` app. The `CustomUser` model extends Django's `AbstractUser`, adding four custom fields: `bio` (TextField), `avatar` (ImageField), `theme_preference` (CharField with choices), and `is_new_user` (BooleanField, default True).

`AUTH_USER_MODEL = 'users.CustomUser'` is set in `settings.py` to instruct Django to use the custom user model throughout the project, including the authentication backend and foreign key relationships.

**Registration** is handled by `RegisterView` (FormView) using a custom `RegisterForm` that extends Django's `UserCreationForm`. On successful validation, the user is created, immediately logged in, and redirected to the home page.

**Login** uses Django's built-in `AuthenticationForm` within a custom `LoginView`. On successful authentication, Django creates a session and sets a session cookie. The `next` query parameter is respected for post-login redirects.

**Profile management** is provided by `ProfileView` (displays stats, reviews, watchlist, history) and `ProfileEditView` (handles bio, avatar, theme updates). Theme switching also has a dedicated AJAX endpoint (`SetThemeView`) that updates `theme_preference` and returns a JSON response for instant client-side updates.

### 6.2 Movie Browsing Module

The `movies` app implements the `HomeView`, `MovieListView`, and `MovieDetailView`.

`HomeView` queries three ordered querysets: top-rated movies (ordered by `avg_rating` descending), trending movies (ordered by `total_watches` descending), and new releases (ordered by `year` descending then `avg_rating`). Each list is limited to 8 movies for the home page carousel.

`MovieListView` retrieves the full movie catalog, applies filters from GET parameters, and paginates at 20 movies per page using Django's `Paginator`. `prefetch_related('genres')` is used to avoid N+1 queries when rendering genre tags.

`MovieDetailView` retrieves a single movie with `prefetch_related('genres', 'reviews__user')`. It computes the current user's review status (`user_review`) and watchlist membership (`in_watchlist`) for conditional rendering. Related movies are identified by `Movie.objects.filter(genres__in=movie.genres.all()).exclude(pk=movie.pk).distinct()[:6]`.

### 6.3 Search and Filtering Module

`SearchView` and the filter portion of `MovieListView` implement the search logic. Title search uses Django's `Q()` objects to construct AND-combined `icontains` filters for each word in the query:

```python
title_q = Q()
for word in q.split():
    title_q &= Q(title__icontains=word)
movies = movies.filter(title_q)
```

This word-by-word AND search means "dark knight" finds movies containing both "dark" and "knight", but not necessarily as an exact phrase. This is more flexible than exact-phrase matching for user queries.

Genre, year range, and minimum rating filters are applied sequentially using ORM chaining. `.distinct()` is called after filtering to prevent duplicates from the many-to-many genre join.

The `SearchForm` provides form field validation and clean data extraction, ensuring type safety (year fields are validated as integers, rating as float).

### 6.4 Review System Module

The `reviews` app handles review creation, update, and deletion. The `AddReviewView.post()` method:
1. Validates the `ReviewForm`.
2. Checks for an existing review by the same user for the same movie (enforcing the one-review-per-user-per-movie constraint).
3. Calls `analyze_sentiment(review_text)` to classify the text.
4. Creates or updates the Review record.
5. Calls `_update_movie_rating(movie)` to recalculate `avg_rating` and `total_ratings` using an aggregate query.
6. Sets `user.is_new_user = False` on first review.
7. Checks whether total reviews is divisible by 50 and triggers SVD retraining if so.

`DeleteReviewView` enforces ownership (only the review author or a staff user can delete) and recalculates the movie's average rating after deletion.

### 6.5 Recommendation Engine Module

The recommendation logic is split between `recommendations/engine.py` and `recommendations/views.py`.

`get_recommendations(user_id, n=20)` loads the serialized SVD model from disk, retrieves the user's latent factor vector and bias, fetches the set of already-rated movie IDs, computes predicted ratings for all unrated candidates, sorts by predicted rating, and returns the top `n` Movie objects.

`RecommendationView` checks `user.is_new_user` and the authentication status to decide between cold-start and personalized paths. For personalized recommendations, the view groups movies by primary genre and selects the top 4 genre groups for display.

### 6.6 Watchlist and Watch History Module

`AddToWatchlistView` uses `get_or_create` on `Watchlist(user, movie)`. If the record already exists, it is deleted (toggle behavior). Both JSON (for AJAX) and redirect (for non-AJAX) responses are supported, checked via the `X-Requested-With: XMLHttpRequest` header.

`RecordWatchView` creates a new `WatchHistory` entry (without uniqueness constraint, so repeat watches are allowed) and atomically increments `total_watches` on the Movie using `F()` expressions to avoid race conditions:

```python
Movie.objects.filter(pk=pk).update(total_watches=F('total_watches') + 1)
```

### 6.7 Admin Panel Module

The `admin_panel` app provides a custom administrative interface protected by the `admin_required` decorator (checks `request.user.is_staff`).

`AdminDashboardView` aggregates statistics using `count()` and `filter()` queries for the summary cards, and fetches top movies, recent users, and recent reviews for the data tables.

`UserManagementView` lists all users with pagination and search. `ToggleUserActiveView` and `ToggleUserStaffView` handle account activation/deactivation and staff privilege grants with safety guards (cannot deactivate self, cannot modify superusers unless also a superuser).

`MovieManagementView`, `AddMovieView`, `EditMovieView`, and `DeleteMovieView` provide full movie CRUD using a `MovieForm` ModelForm.

`RetrainView` accepts POST requests with checkboxes for SVD and sentiment retraining. It calls the appropriate training functions, captures their results, and renders a results page showing success/failure/accuracy for each model.

---

## Chapter 7: Machine Learning Components

### 7.1 SVD Collaborative Filtering

**Mathematical Foundation:**

Given a user-item rating matrix R where R[u][i] is user u's rating of item i, SVD factorization approximates R as:

```
R̂[u][i] = μ + b_u + b_i + p_u · q_i^T
```

Where:
- **μ** = global average rating across all user-item pairs
- **b_u** = user bias (user u's tendency to rate above/below average)
- **b_i** = item bias (item i's tendency to receive above/below average ratings)
- **p_u** ∈ ℝ^k = user u's latent factor vector (k-dimensional representation of user preferences)
- **q_i** ∈ ℝ^k = item i's latent factor vector (k-dimensional representation of item characteristics)

The latent factors p_u and q_i capture abstract features. In a movie recommendation context, a factor might loosely correspond to a genre preference, directorial style preference, or era preference — though these are not explicitly interpretable.

**Optimization:**

The model is trained by minimizing the regularized squared error over all known ratings:

```
min_{p*, q*, b*} Σ_{(u,i)∈K} (R[u][i] − μ − b_u − b_i − p_u · q_i^T)² + λ(||p_u||² + ||q_i||² + b_u² + b_i²)
```

where K is the set of observed (user, item) rating pairs and λ is the regularization coefficient.

**Stochastic Gradient Descent (SGD) Updates:**

For each observed rating (u, i, r), the prediction error is computed as:

```
e_ui = r - (μ + b_u + b_i + p_u · q_i^T)
```

Then the parameters are updated:

```
b_u ← b_u + α(e_ui − λ · b_u)
b_i ← b_i + α(e_ui − λ · b_i)
p_u ← p_u + α(e_ui · q_i − λ · p_u)
q_i ← q_i + α(e_ui · p_u − λ · q_i)
```

where α is the learning rate.

**Hyperparameters used in NextReel:**

| Parameter | Value | Rationale |
|---|---|---|
| `n_factors` (k) | 50 | Balance between expressiveness and overfitting risk; standard value for medium-sized datasets. |
| `n_epochs` | 30 | Sufficient convergence for typical dataset sizes without over-training. |
| `learning_rate` (α) | 0.005 | Conservative learning rate to ensure stable convergence. |
| `regularization` (λ) | 0.02 | Standard L2 regularization value from literature. |
| Random seed | 42 | Reproducibility of factor initialization. |

**Model Serialization:**

After training, the model is serialized using Python's `pickle` module into a `.pkl` file containing the dictionary:

```python
{
    'user_factors': user_factors,   # shape: (n_users, n_factors)
    'item_factors': item_factors,   # shape: (n_items, n_factors)
    'user_index': user_index,       # dict: user_id → row index
    'item_index': item_index,       # dict: movielens_id → col index
    'global_mean': global_mean,     # scalar float
    'user_bias': user_bias,         # shape: (n_users,)
    'item_bias': item_bias,         # shape: (n_items,)
    'n_factors': n_factors,         # scalar int
}
```

This structure allows O(1) user/item lookup and O(k) prediction computation.

### 7.2 Naive Bayes Sentiment Analysis with TF-IDF

**Multinomial Naive Bayes:**

Naive Bayes classifiers are probabilistic classifiers based on Bayes' theorem. The Multinomial variant is appropriate for text classification where features represent word occurrence counts:

```
P(class | document) ∝ P(class) · Π P(word_i | class)
```

Taking the log for numerical stability:

```
log P(class | document) = log P(class) + Σ count(word_i) · log P(word_i | class)
```

Each word's conditional probability is estimated with Laplace smoothing (α = 0.5 in NextReel) to handle unseen words:

```
P(word_i | class) = (count(word_i in class) + α) / (total words in class + α · vocabulary size)
```

**Feature Extraction with CountVectorizer:**

Raw review text is preprocessed (HTML tag removal, lowercasing, special character removal) and then converted to a term frequency vector by CountVectorizer. The vectorizer:
- Builds a vocabulary of the top 20,000 most frequent terms.
- Removes English stop words.
- Considers both unigrams and bigrams (`ngram_range=(1, 2)`), capturing phrases like "not good" that single-word analysis would misinterpret.
- Transforms new reviews using the learned vocabulary mapping.

**Confidence Threshold:**

After prediction, the model also computes class probabilities via `predict_proba()`. If the maximum probability is below 0.6, the review is classified as "neutral" regardless of the predicted class. This avoids overconfident misclassification of ambiguous text.

**Fallback Heuristic:**

When the model files are unavailable, a keyword-based heuristic is used. It counts the intersection of the review words with predefined positive and negative word sets (approximately 18 words each) and returns the dominant sentiment. This ensures the review submission workflow is never blocked by a missing model.

### 7.3 Training Process

**SVD Training Process:**

1. Load all `Review` records from the database into a Pandas DataFrame.
2. Convert user IDs and MovieLens IDs to string keys; build integer index maps.
3. Initialize latent factor matrices with `np.random.normal(0, 0.1)` and biases at zero.
4. For each epoch (30 total): shuffle ratings; iterate through each (user, item, rating) triple; compute error; apply SGD updates.
5. Print RMSE every 5 epochs as a convergence diagnostic.
6. Save the trained model dict to `svd_model.pkl`.

**Sentiment Training Process:**

1. Load the IMDB dataset CSV and identify text and label columns.
2. Preprocess all review texts (HTML stripping, lowercasing, non-alpha removal).
3. Normalize label values to `'positive'` / `'negative'` using a mapping dict.
4. Split into 80% train / 20% test using `train_test_split(random_state=42)`.
5. Fit `CountVectorizer` on training data; transform both sets.
6. Fit `MultinomialNB(alpha=0.5)` on training features.
7. Evaluate on test set; print accuracy.
8. Save both the model and vectorizer as separate `.pkl` files.

### 7.4 Model Evaluation

**SVD Evaluation:**

The primary training-time metric is **Root Mean Squared Error (RMSE)** on the training set, printed every 5 epochs. RMSE measures the average magnitude of prediction errors in rating units (1–5 scale). A final RMSE in the range of 0.85–1.0 is typical for this dataset size and hyperparameter configuration.

Note that NextReel does not implement a held-out test set for SVD evaluation. For a more rigorous evaluation, k-fold cross-validation should be applied. This is identified as a future improvement.

**Sentiment Evaluation:**

The sentiment classifier is evaluated on a held-out 20% test set using **accuracy score** (proportion of correctly classified reviews). The expected accuracy on the IMDB dataset is approximately **70–87%** depending on the dataset size used.

The classification is binary at the model level (positive/negative); the "neutral" label is applied post-hoc when model confidence is below 0.6.

### 7.5 Cold-Start Problem and Fallback Strategy

The cold-start problem refers to the inability to generate personalized recommendations for new users with no rating history. NextReel addresses this with a three-tier fallback strategy:

| Condition | Behavior |
|---|---|
| Unauthenticated user | Show trending, top-rated, and new releases. |
| Authenticated, `is_new_user = True` | Show same cold-start lists. |
| Authenticated, has ratings, user not in SVD model index | Fall back to top-rated movies. |
| SVD model file missing or corrupted | Fall back to top-rated movies. |
| Exception during prediction | Fall back to top-rated movies. |

The `is_new_user` flag is set to `False` automatically when the user submits their first review, at which point they become eligible for personalized recommendations on the next model retraining cycle.

---

## Chapter 8: Testing

### 8.1 Types of Testing

**Manual Functional Testing:** All major user flows were tested manually through the browser interface to verify correct behavior.

**Unit-Level Testing (Manual):** Individual functions such as `analyze_sentiment()`, `get_recommendations()`, and `_update_movie_rating()` were tested in the Django shell with sample inputs.

**Integration Testing:** The interaction between modules (e.g., review submission triggering sentiment analysis and average rating recalculation) was verified end-to-end.

**Edge Case Testing:** Boundary conditions such as empty search queries, missing model files, users with no reviews, and deletion cascades were explicitly tested.

**Cross-Browser Testing:** The UI was verified on Chrome, Firefox, and Edge to ensure consistent rendering of both themes.

### 8.2 Functional Test Cases

| ID | Test Case | Input | Expected Output | Result |
|---|---|---|---|---|
| TC-01 | User Registration | Valid username, email, password | Account created, user logged in, redirect to home | Pass |
| TC-02 | Registration with duplicate username | Existing username | Form error: "Username already taken" | Pass |
| TC-03 | Login with correct credentials | Valid username and password | User logged in, session created | Pass |
| TC-04 | Login with wrong password | Incorrect password | Form error: invalid credentials | Pass |
| TC-05 | Browse movies (first page) | GET /movies/ | 20 movies displayed, pagination shown | Pass |
| TC-06 | Filter by genre | Genre = "Action" | Only Action movies shown | Pass |
| TC-07 | Search by title | Query = "matrix" | Movies with "matrix" in title shown | Pass |
| TC-08 | Search by year range | Year 2000–2005 | Only movies from that range shown | Pass |
| TC-09 | View movie detail | Click on a movie card | Detail page with title, genres, reviews shown | Pass |
| TC-10 | Submit a review | Rating = 4, text = "Great movie" | Review saved, avg_rating updated | Pass |
| TC-11 | Duplicate review submission | Same user, same movie | Existing review updated, not duplicated | Pass |
| TC-12 | Sentiment on positive text | "This was a wonderful and amazing film" | Classified as "positive" | Pass |
| TC-13 | Sentiment on negative text | "Terrible waste of time, boring and awful" | Classified as "negative" | Pass |
| TC-14 | Add to watchlist | Click "Add to Watchlist" | Movie added, button changes to "Remove" | Pass |
| TC-15 | Remove from watchlist | Click "Remove from Watchlist" | Movie removed, button reverts | Pass |
| TC-16 | Mark as watched | Click "Mark as Watched" | WatchHistory entry created, total_watches incremented | Pass |
| TC-17 | View recommendations (new user) | User with no reviews visits /recommendations/ | Cold-start lists shown (trending, top-rated, new) | Pass |
| TC-18 | View recommendations (active user) | User with reviews visits /recommendations/ | SVD-based personalized recommendations grouped by genre | Pass |
| TC-19 | Access admin panel as non-staff | Regular user navigates to /admin-panel/ | Redirected to login or 403 error | Pass |
| TC-20 | Access admin panel as staff | Staff user navigates to /admin-panel/ | Dashboard loaded successfully | Pass |
| TC-21 | Deactivate a user | Admin clicks Deactivate on a user | User's is_active set to False | Pass |
| TC-22 | Deactivated user tries to login | Deactivated account | Login rejected with error message | Pass |
| TC-23 | Import movies from CSV | python manage.py import_movies | Movies and genres created in database | Pass |
| TC-24 | Train SVD model | python manage.py train_svd | Model file created at SVD_MODEL_PATH | Pass |
| TC-25 | Train sentiment model | python manage.py train_sentiment | Model and vectorizer pkl files created | Pass |
| TC-26 | Delete a review | Owner clicks Delete on review | Review deleted, avg_rating recalculated | Pass |
| TC-27 | Non-owner tries to delete review | Different user clicks delete endpoint | Permission denied, redirect to movie page | Pass |
| TC-28 | Theme switch (Dark → Warm) | User selects Warm Glow theme and saves | Profile updated, Warm theme applied | Pass |

### 8.3 Edge Cases and Boundary Testing

| Scenario | Expected Behavior | Result |
|---|---|---|
| SVD model file missing | Recommendations fall back to top-rated movies | Pass |
| Sentiment model file missing | Sentiment falls back to keyword heuristic | Pass |
| User rates a movie not in MovieLens dataset | Movie predicted using avg_rating (no SVD factors) | Pass |
| All movies already rated by a user | Empty candidate list → top-rated fallback | Pass |
| Review submitted with total review count = 50 | SVD retraining triggered silently | Pass |
| SVD retrain fails (exception) | Exception caught; review still saved successfully | Pass |
| Import movies CSV with missing ratings.csv | Import proceeds with avg_rating = 0, warning printed | Pass |
| Search with empty query string | All movies shown (no title filter applied) | Pass |
| Year filter with non-integer value | Filter silently ignored, all movies shown | Pass |
| User submits review with only whitespace | Form validation error (required field) | Pass |
| Admin tries to deactivate own account | Error message: "You cannot deactivate your own account" | Pass |

---

## Chapter 9: Results and UI Description

### 9.1 Home Page

The Home Page (`/`) presents a visually striking entry point with the NextReel branding at the top. The navigation bar includes links to Browse Movies, Search, and Recommendations, with login/register buttons for unauthenticated users or a user dropdown with profile/logout links for authenticated users.

Below the hero section, three horizontal carousels display "Top Rated," "Trending Now," and "New Releases" movies, each showing 8 movie cards. Each card features the movie poster (or a stylized default SVG when no poster is available), the title, the release year, and a five-star rating display. Cards are clickable and navigate to the Movie Detail page.

In Cinematic Dark mode, the page uses deep charcoal and black backgrounds with gold star icons and warm amber accent colors, evoking the atmosphere of a cinema. The Warm Glow theme substitutes a warm cream-and-brown palette.

### 9.2 Movie Browse and Search Pages

The Browse page (`/movies/`) displays a full-width grid of movie cards with a sidebar or top filter panel. The current page number and total movie count are displayed. Genre buttons allow one-click genre filtering. The pagination controls at the bottom allow navigation through the catalog.

The Search page (`/movies/search/`) is dedicated to advanced discovery. The search form is prominently displayed with all filter options (title, genre, year from/to, min rating). Results appear below the form with the same card grid layout. When a search is active, the active filter parameters are shown as removable tags and the result count is prominently displayed (e.g., "47 movies found").

### 9.3 Movie Detail Page

The Movie Detail page is divided into a prominent header and a tabbed content area.

The **header** occupies the upper portion with the movie poster on the left and metadata on the right: full title, year, genre tags (displayed as pill badges), average star rating, total rating count, and action buttons (Add to Watchlist, Mark as Watched). The poster uses a consistent aspect ratio; missing posters are replaced by a stylized camera-and-reel SVG with the movie title overlaid.

The **tabbed section** contains:
- **Overview tab:** Full description text and a repeat of the genre listing.
- **Reviews tab:** A list of user review cards, each showing the reviewer's avatar, username, star rating, review text, sentiment badge (green/positive, red/negative, grey/neutral), and timestamp. A review submission form appears at the bottom for logged-in users (or a prompt to log in for guests). If the current user has already reviewed the movie, their review is highlighted and a delete button is shown.
- **Related Movies tab:** A horizontal scroll of up to 6 related movie cards based on shared genres.

### 9.4 Recommendations Page

The Recommendations page (`/recommendations/`) has two distinct visual states:

**Cold-start state** (new/unauthenticated users): Three clearly labeled sections — "Trending Now," "Top Rated," and "New Releases" — each showing a grid of 12 movie cards. A prominent banner at the top explains that personalized recommendations will appear after the user rates some movies and links to the Browse page.

**Personalized state** (users with reviews): Up to four genre sections are displayed, each with a heading (the genre name), a short description, and a row of recommended movies ordered by predicted rating. The section headers use genre-appropriate styling. A note at the bottom explains that the recommendations are powered by collaborative filtering and will improve with more ratings.

### 9.5 User Profile Page

The Profile page is organized into a sidebar with the user's avatar, username, email, bio, member since date, and an "Edit Profile" button, and a main content area with three tabbed sections: My Reviews, My Watchlist, and Watch History.

**My Reviews** shows a compact list of the user's 20 most recent reviews with the movie title, rating, sentiment badge, review excerpt, and a delete button.

**My Watchlist** shows the 20 most recently added watchlist movies as thumbnail cards with a "Remove" button on each.

**Watch History** shows the 20 most recently recorded watches with the movie title and the date/time watched.

A stats row at the top of the main area shows total reviews written, and the breakdown of positive vs. negative sentiment counts with a simple progress bar visualization.

### 9.6 Admin Panel

The Admin Dashboard presents six summary stat cards at the top (total users, movies, reviews, positive/negative/neutral review counts) followed by three data tables: Top 10 Movies (sorted by rating), Recent Users, and Recent Reviews.

The Users Management page is a sortable, searchable list with inline action buttons for each user. Color-coded badges indicate active/inactive and staff/non-staff status.

The Movies Management page is similar, with filter controls for genre and a search bar. The Add/Edit Movie forms include all Movie model fields with a drag-and-drop image upload for the poster.

The Retrain Models page presents a clear form with two sections (SVD and Sentiment), each with a checkbox, a brief description of what will happen, and a dataset path input for the sentiment model. After submission, results are displayed with colored success/warning/error banners.

---

## Chapter 10: Conclusion and Future Work

### 10.1 Conclusion

NextReel successfully demonstrates the integration of machine learning techniques into a full-stack web application built with Django. The system addresses the primary objective of delivering personalized movie recommendations through SVD collaborative filtering, while the Naive Bayes sentiment classifier adds qualitative depth to the review system by automatically categorizing user opinions.

The cold-start problem, a fundamental challenge in recommender system design, is handled gracefully through a tiered fallback mechanism that ensures new and unauthenticated users always receive useful content. Model persistence through pickle serialization and automatic background retraining every 50 new reviews demonstrates a practical approach to keeping ML models current in a production-like environment.

The two-theme CSS design, the custom administrative dashboard, and the MovieLens data import pipeline round out the system into a complete, deployable application that addresses real-world concerns beyond the academic ML component.

The project confirms that SVD collaborative filtering is an effective and computationally tractable approach for personalized recommendation even when implemented from scratch with NumPy, achieving reasonable RMSE on the MovieLens dataset. The Naive Bayes sentiment classifier provides a useful and fast classification baseline for review text at approximately 70–87% accuracy.

### 10.2 Future Work

The following enhancements are identified as natural extensions to the NextReel system:

1. **PostgreSQL migration:** Replace SQLite with PostgreSQL or MySQL to support concurrent users and enable production deployment.

2. **Transformer-based sentiment analysis:** Replace the Naive Bayes classifier with a fine-tuned BERT or RoBERTa model for significantly improved sentiment accuracy, particularly for sarcasm and mixed-sentiment reviews.

3. **Implicit feedback integration:** Incorporate watch history and watchlist additions as implicit rating signals in the SVD model (using confidence-weighted matrix factorization such as ALS), rather than relying solely on explicit 1–5 star ratings.

4. **Real-time recommendation pre-computation:** Pre-compute and cache recommendation vectors for all users at model retraining time, serving recommendations from cache to eliminate per-request latency.

5. **TMDB/OMDB API integration:** Pull movie posters, trailers, cast, crew, and detailed plot data from The Movie Database (TMDB) API to enrich the movie detail pages.

6. **Content-based filtering layer:** Build a proper content-based filtering component using TF-IDF on movie descriptions and metadata, and combine it with the SVD CF model in a hybrid architecture for improved cold-start handling.

7. **Social features:** Friend lists, activity feeds ("your friend rated X"), and shared watchlists to leverage social signals in recommendations.

8. **Mobile-responsive design:** Optimize the CSS grid and layouts for small screen sizes, or develop a companion mobile application.

9. **Recommendation explanations:** Display "Why was this recommended?" explanations (e.g., "Because you liked The Dark Knight") using the top contributing user factors or similar-user analysis.

10. **A/B testing framework:** Implement a mechanism to compare recommendation strategies (SVD vs. content-based vs. popularity) across different user segments and measure click-through and watch completion rates.

11. **Asynchronous model retraining:** Move SVD retraining to a background task queue (e.g., Celery with Redis) to prevent any potential latency impact during the 50th-review trigger event.

12. **Formal evaluation framework:** Implement proper train/test split or k-fold cross-validation for SVD evaluation, reporting Precision@K, Recall@K, and NDCG@K metrics in addition to RMSE.

---

## References

[1] Gomez-Uribe, C. A., & Hunt, N. (2015). The Netflix Recommender System: Algorithms, Business Value, and Innovation. *ACM Transactions on Management Information Systems (TMIS)*, 6(4), 1–19.

[2] Koren, Y., Bell, R., & Volinsky, C. (2009). Matrix Factorization Techniques for Recommender Systems. *IEEE Computer*, 42(8), 30–37.

[3] Koren, Y. (2008). Factorization Meets the Neighborhood: A Multifaceted Collaborative Filtering Model. In *Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 426–434).

[4] Funk, S. (2006). Netflix Update: Try This at Home. *Simon Funk's Blog*. Retrieved from https://sifter.org/~simon/journal/20061211.html

[5] Burke, R. (2002). Hybrid Recommender Systems: Survey and Experiments. *User Modeling and User-Adapted Interaction*, 12(4), 331–370.

[6] Steck, H., Baltrunas, L., Elahi, E., Liang, D., Raiber, F., & Basilico, J. (2021). Deep Learning for Recommender Systems: A Netflix Case Study. *AI Magazine*, 42(3), 7–18.

[7] Liu, B. (2012). *Sentiment Analysis and Opinion Mining*. Morgan & Claypool Publishers.

[8] McCallum, A., & Nigam, K. (1998). A Comparison of Event Models for Naive Bayes Text Classification. In *AAAI Workshop on Learning for Text Categorization*, 41(1), 41–48.

[9] Pang, B., Lee, L., & Vaithyanathan, S. (2002). Thumbs up? Sentiment Classification Using Machine Learning Techniques. In *Proceedings of the 2002 Conference on Empirical Methods in Natural Language Processing (EMNLP)* (pp. 79–86).

[10] Harper, F. M., & Konstan, J. A. (2015). The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems*, 5(4), 1–19.

[11] Ricci, F., Rokach, L., & Shapira, B. (Eds.). (2015). *Recommender Systems Handbook* (2nd ed.). Springer.

[12] Django Software Foundation. (2023). *Django Documentation: Version 4.2*. Retrieved from https://docs.djangoproject.com/en/4.2/

[13] Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

---

## Defense Q&A Section

The following 25 questions represent the types of questions a defense committee is likely to ask. Questions span conceptual understanding, technical implementation, design decisions, machine learning theory, security, limitations, and future directions.

---

### Q1. What is Singular Value Decomposition (SVD), and how does it work in your recommendation engine?

**Answer:**

Singular Value Decomposition is a linear algebra technique that factorizes a matrix M into three matrices: M = UΣVᵀ, where U and V are orthogonal matrices and Σ is a diagonal matrix of singular values. In the context of recommender systems, we apply this concept to the user-item rating matrix to discover latent features.

However, true mathematical SVD cannot be directly applied to sparse matrices because it requires all entries to be known. In NextReel, I use **FunkSVD** (also called Matrix Factorization), which learns user factor matrix P and item factor matrix Q through stochastic gradient descent (SGD) without ever computing the full matrix. The prediction formula is:

```
R̂[u][i] = μ + b_u + b_i + P[u] · Q[i]ᵀ
```

Where μ is the global mean rating, b_u is a user bias term, b_i is an item bias term, and the dot product of P[u] and Q[i] captures the interaction between the user's latent preferences and the item's latent characteristics.

SGD iterates over each observed (user, item, rating) triple, computes the prediction error, and updates all parameters in the direction that reduces the error while applying L2 regularization to prevent overfitting. After 30 epochs, the learned vectors are saved and used to predict ratings for unobserved movie-user pairs.

In practice, the 50-dimensional factor vectors might loosely capture concepts like "preference for action movies" or "preference for critically acclaimed films," but the factors are not interpretable in human terms — they are abstract mathematical representations that the optimization process discovers from the rating patterns.

---

### Q2. Why did you choose Django over other web frameworks like Flask or FastAPI?

**Answer:**

Django was the right choice for NextReel for several concrete reasons:

**Batteries-included:** Django provides an ORM, authentication system, form validation, CSRF protection, session management, URL routing, an admin interface, and a template engine out of the box. Building the same features in Flask would have required selecting and integrating multiple third-party libraries, increasing complexity and potential security risks.

**ORM power:** Django's ORM handles complex queries (filtering, annotation, aggregation, prefetch_related for N+1 prevention) in a clean, Pythonic way. It also abstracts the database backend, making a future migration from SQLite to PostgreSQL a one-line change in settings.

**AUTH_USER_MODEL:** Django's built-in authentication system supports custom user models through `AbstractUser`, which is exactly what I needed to add bio, avatar, and theme_preference fields to the user.

**Class-Based Views:** CBVs provide built-in mixins like `LoginRequiredMixin` that cleanly handle authentication requirements without repeating conditional logic in every view.

**LTS release:** Django 4.2 is a Long-Term Support release, meaning security patches for several years.

Flask would have been appropriate for a smaller, API-only service or microservice. FastAPI would have been excellent for a high-performance async API, but it requires a separate frontend framework, which would have significantly increased project complexity for what is fundamentally a server-rendered web application.

---

### Q3. Why did you use SQLite instead of PostgreSQL or MySQL?

**Answer:**

SQLite was the appropriate choice for an academic project for these reasons:

1. **Zero configuration:** SQLite requires no server process, no connection string configuration, and no separate installation. The entire database is a single file (`db.sqlite3`) that Django manages automatically. For a development and demonstration environment, this significantly simplifies setup.

2. **Portability:** The database is a file that can be copied, backed up, or shared. This is ideal for academic submission.

3. **Django default:** Django's default database configuration is SQLite, and all development workflows (migrations, management commands) work seamlessly with it.

4. **Appropriate for scope:** NextReel is a single-user or low-traffic academic demonstration. SQLite's limitations (no concurrent writes, file-level locking) are not relevant at this scale.

The design is not locked into SQLite. Django's ORM is database-agnostic. Migrating to PostgreSQL for a production deployment requires only changing two lines in `settings.py` — the ENGINE to `django.db.backends.postgresql` and adding connection parameters. No model, view, or template code would need to change. This is one of the key benefits of using Django's ORM abstraction layer.

---

### Q4. What is the cold-start problem, and how does your system handle it?

**Answer:**

The cold-start problem occurs when a recommendation system cannot generate personalized recommendations because it lacks sufficient data about a user (new-user cold-start) or an item (new-item cold-start).

In NextReel, the cold-start problem manifests for new users who have not yet submitted any reviews. The SVD model has learned latent factors from historical ratings, but a new user has no factor vector — the system does not know where to place them in the latent factor space.

**How NextReel handles it:**

1. **is_new_user flag:** When a user registers, `is_new_user = True`. The recommendations view checks this flag.

2. **Cold-start content:** If `is_new_user` is True (or the user is not authenticated), the system returns three curated lists derived from aggregate statistics: trending movies (highest `total_watches`), top-rated movies (highest `avg_rating`), and new releases (highest `year`). These are popularity-based recommendations that do not require any user-specific data.

3. **Transition to personalized:** When the user submits their first review, `is_new_user` is set to False. On the next model retraining cycle, the user's ratings will be incorporated, and their latent factor vector will be learned. From that point forward, they receive SVD-based personalized recommendations.

4. **Additional fallbacks:** Even for non-new users, if the SVD model is missing, fails to load, or the user's ID is not in the model's user index (e.g., they registered after the last training run), the system transparently falls back to top-rated movies.

The item cold-start (movies without ratings) is handled by using `movie.avg_rating` as the predicted score for movies whose `movielens_id` is not in the SVD model's item index.

---

### Q5. Explain the sentiment analysis pipeline from raw text to a classification label.

**Answer:**

The full pipeline in `reviews/sentiment.py` operates in these steps:

**Step 1 — Preprocessing (`preprocess_text`):**
- Remove HTML tags using regex `<[^>]+>` (common in scraped text).
- Convert to lowercase.
- Remove all non-alphabetic characters.
- Collapse multiple spaces.

**Step 2 — Feature extraction (CountVectorizer):**
The preprocessed text is transformed into a sparse vector where each dimension corresponds to a vocabulary term. The vocabulary was learned during training from the IMDB dataset (top 20,000 terms, unigrams and bigrams, English stop words removed). The value at each dimension is the count of that term in the review.

**Step 3 — Classification (MultinomialNB):**
The count vector is passed to the trained Naive Bayes model. The model computes the log posterior probability for each class (positive/negative) using the formula:
`log P(class | doc) = log P(class) + Σ count(w) · log P(w | class)`
The class with the higher log probability is selected.

**Step 4 — Confidence check:**
`predict_proba()` returns a probability array for each class. If `max(probabilities) < 0.6`, the review is classified as "neutral" regardless of which class won. This prevents overconfident misclassification of ambiguous reviews.

**Step 5 — Fallback:**
If the model files are missing, a keyword heuristic scans for words in predefined positive/negative word sets and returns the dominant sentiment.

The final label ("positive", "negative", or "neutral") is stored in the `Review.sentiment` field.

---

### Q6. What security measures does your application implement?

**Answer:**

NextReel leverages Django's built-in security framework, which addresses several OWASP Top 10 vulnerabilities:

1. **CSRF Protection:** All state-changing forms (POST requests) include Django's CSRF token (`{% csrf_token %}`). Django's `CsrfViewMiddleware` validates the token on every POST request and rejects requests with invalid or missing tokens. This prevents cross-site request forgery attacks.

2. **Password Hashing:** Django's authentication system uses PBKDF2 with SHA-256 and a per-user salt by default. Passwords are never stored in plaintext. Django also enforces configurable password validators (minimum length, common password list, numeric-only rejection, attribute similarity).

3. **SQL Injection Prevention:** The Django ORM uses parameterized queries for all database interactions. Raw SQL is never used in the project. The ORM's `Q()` objects, `.filter()`, `.get()`, etc. all produce safe parameterized SQL, making SQL injection impossible through normal ORM usage.

4. **XSS Protection:** Django's template engine auto-escapes all variables by default. User-supplied content rendered in templates is HTML-escaped. The `X-XSS-Protection` header is set by Django's `SecurityMiddleware`.

5. **Clickjacking Protection:** Django's `XFrameOptionsMiddleware` sets the `X-Frame-Options: DENY` header, preventing the application from being embedded in iframes.

6. **Authentication Guards:** The `LoginRequiredMixin` (for CBVs) and the custom `admin_required` decorator protect all authenticated-only endpoints. Unauthenticated access to protected pages results in a redirect to the login page.

7. **Ownership Verification:** The `DeleteReviewView` explicitly verifies that `review.user == request.user` before allowing deletion, preventing users from deleting other users' reviews.

For a production deployment, additional hardening steps would be required: `DEBUG = False`, a strong `SECRET_KEY` stored in environment variables, HTTPS enforcement, and proper `ALLOWED_HOSTS` configuration.

---

### Q7. How does your search functionality work? Why did you implement word-by-word AND matching instead of full-text search?

**Answer:**

The search uses Django ORM `Q()` objects to construct an AND-combined query. For a query like "dark knight", the code builds:

```python
title_q = Q(title__icontains='dark') & Q(title__icontains='knight')
```

This returns movies whose titles contain both "dark" and "knight" in any position and order, rather than the exact phrase "dark knight." The `icontains` lookup is case-insensitive.

**Reasons for this approach over exact-phrase search:**

1. **Flexibility:** Users often misremember exact titles. "knight dark" still finds "The Dark Knight" because both words must be present, regardless of order.

2. **Simplicity:** No external full-text search engine (Elasticsearch, Whoosh, PostgreSQL full-text) is required. The ORM-level implementation works identically on SQLite and PostgreSQL.

3. **Appropriate for the dataset:** Movie titles are relatively short and distinct. For a catalog of ~10,000 movies, ORM-level string matching is fast enough.

**Limitations of this approach:**

- It does not support stemming (searching "run" won't find "running").
- It does not handle typos or fuzzy matching.
- For very large datasets, `LIKE '%word%'` queries are slow because they cannot use B-tree indexes.

For a production system with millions of movies, migrating to PostgreSQL's `pg_trgm` extension or Elasticsearch would provide much better search quality and performance. This is noted in the Future Work section.

---

### Q8. What is the `is_new_user` flag, and when does it change?

**Answer:**

`is_new_user` is a `BooleanField` on `CustomUser` with `default=True`. It represents whether the user has submitted at least one rating/review.

It changes from `True` to `False` in `AddReviewView.post()`, immediately after a successful review (or review update) is saved:

```python
if request.user.is_new_user:
    request.user.is_new_user = False
    request.user.save(update_fields=['is_new_user'])
```

`update_fields=['is_new_user']` is used for efficiency — it issues an UPDATE statement for only that column rather than re-saving the entire user record.

The flag serves as the gating condition in `RecommendationView`: if `is_new_user is True`, the user sees cold-start recommendations. Once it becomes False, the user receives SVD-based personalized recommendations (assuming the SVD model has been trained with their data).

Note: There is a brief window where `is_new_user` is False but the user's data has not yet been incorporated into the SVD model (because retraining happens every 50 reviews). During this window, the user falls through to the second fallback in `get_recommendations()`: checking whether the user's ID is in the model's `user_index` dictionary. If not found, the function returns top-rated movies.

---

### Q9. How does the automatic SVD retraining work?

**Answer:**

The automatic retraining is triggered inside `AddReviewView.post()`, after every new review or review update is saved:

```python
total_reviews = Review.objects.count()
if total_reviews % 50 == 0:
    try:
        from recommendations.engine import train_svd_model
        train_svd_model()
    except Exception:
        pass
```

When the total number of reviews in the database is exactly divisible by 50, `train_svd_model()` is called. It reads all current reviews, trains a new SVD model, and saves the updated `.pkl` file, overwriting the previous model.

**Design decisions:**

1. **Non-blocking:** The entire retraining call is wrapped in a `try/except Exception: pass`. If retraining fails for any reason (insufficient data, memory error, disk full), the review submission still completes successfully. The user is not affected.

2. **Synchronous in current implementation:** The retraining runs in the same request thread, which means the 50th, 100th, etc. review submissions will experience slightly longer response times during retraining. For a production system, this should be moved to a Celery background task.

3. **Modulo 50 trigger:** This is a heuristic based on the assumption that 50 new ratings represent enough new information to justify the compute cost of retraining. The threshold is configurable and could be tuned based on observed dataset growth.

4. **Full retraining:** Each trigger performs a full retrain from all available data rather than incremental updates. Incremental SVD updates are mathematically more complex and were out of scope for this project.

---

### Q10. Explain the movie average rating update mechanism. Why do you use `F()` expressions?

**Answer:**

When a review is created, updated, or deleted, `_update_movie_rating(movie)` is called:

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

This uses a database-level aggregate query (`AVG()` and `COUNT()` in SQL) to compute the correct values from all current reviews. This is accurate and idempotent — running it multiple times produces the same result.

The `F()` expression is used separately for incrementing `total_watches` in `RecordWatchView`:

```python
Movie.objects.filter(pk=pk).update(total_watches=F('total_watches') + 1)
```

`F()` expressions are important here because they translate directly to `UPDATE movies SET total_watches = total_watches + 1 WHERE id = %s` in SQL. This is an **atomic operation** at the database level.

The alternative — reading `movie.total_watches`, incrementing in Python, then saving — is vulnerable to a race condition: if two users click "Mark as Watched" for the same movie at nearly the same time, both requests could read the same value (e.g., 100), both increment to 101, and both save 101, losing one count. The `F()` expression lets the database handle the increment atomically, eliminating this race condition.

---

### Q11. How does the `prefetch_related` optimization work, and where do you use it?

**Answer:**

`prefetch_related` is a Django ORM optimization that addresses the N+1 query problem in many-to-many and reverse foreign-key relationships.

Without optimization, rendering a page with 20 movies, each showing their genre tags, would execute:
- 1 query to fetch the 20 movies
- 20 additional queries (one per movie) to fetch each movie's genres

Total: 21 queries. For 100 movies: 101 queries.

With `prefetch_related('genres')`, Django executes:
- 1 query to fetch the movies
- 1 additional query to fetch all genres for those movies at once: `SELECT * FROM genres WHERE id IN (...)`
- Django then maps genre records to movie records in Python memory.

Total: 2 queries regardless of page size.

In NextReel, `prefetch_related` is used in:
- `MovieListView`: `Movie.objects.all().prefetch_related('genres')` — for the browse page grid.
- `SearchView`: same pattern for the search results page.
- `MovieDetailView`: `Movie.objects.prefetch_related('genres', 'reviews__user')` — fetches genres and review-author data together.
- `AdminMovieManagementView`: `Movie.objects.prefetch_related('genres')` — for the admin movie list.

Additionally, `select_related` is used for foreign-key (single-object) relationships in profile views: `Review.objects.select_related('movie')`, which performs a SQL JOIN rather than a separate query, fetching the related movie in the same query.

---

### Q12. What happens if two users try to review the same movie at the exact same time?

**Answer:**

The `Review` model has a `unique_together = ('user', 'movie')` database constraint. This means the database itself enforces that each (user, movie) pair has at most one review.

At the view level, `AddReviewView` checks for an existing review using `Review.objects.filter(user=request.user, movie=movie).first()`. If found, it updates the existing record rather than creating a new one. If not found, it creates a new review.

For **two different users** reviewing the same movie simultaneously, this is not a problem — each (user_A, movie) and (user_B, movie) pair is distinct, so both reviews can be created concurrently.

For **the same user** submitting the review form twice (double-click, browser back button, etc.), the behavior depends on timing:
- If the first request completes before the second arrives: the first creates the review, the second updates it (since `filter().first()` now returns the created record).
- If both arrive simultaneously before either completes: one request will encounter a `django.db.IntegrityError` due to the database-level `UNIQUE` constraint violation. This edge case is not explicitly handled in the current code with a try/except, which is a minor robustness gap. In production, wrapping the create operation in a `try/except IntegrityError` and retrying as an update would be the correct fix. This is noted as a known limitation.

The `_update_movie_rating()` function recalculates from all reviews using an aggregate query, so it remains consistent regardless of concurrent review submissions.

---

### Q13. What is the difference between `avg_rating` stored on the Movie model and calculating it dynamically from reviews? Why store it?

**Answer:**

`avg_rating` is a **denormalized** (redundantly stored) field. The "normalized" approach would be to always compute it on the fly using `Movie.objects.annotate(avg=Avg('reviews__rating'))`.

**Why store it instead:**

1. **Read performance:** The home page, browse page, search results, and recommendation lists all display and sort by `avg_rating`. If computed dynamically, each page load for 20 movies would require a `GROUP BY` aggregate JOIN across the reviews table. Storing the value as a simple column allows `ORDER BY avg_rating` to use a B-tree index efficiently.

2. **Sorting and filtering:** `Movie.objects.filter(avg_rating__gte=4.0)` and `Movie.objects.order_by('-avg_rating')` are simple column comparisons, not aggregate queries. This is critical for fast pagination and filtering.

3. **Staleness risk (managed):** The trade-off is that `avg_rating` can become stale if not updated properly. NextReel mitigates this by always calling `_update_movie_rating()` after every review creation, update, and deletion — three operations that trigger the recalculation. The denormalized value is thus always consistent within the same request cycle.

**When dynamic computation is better:** For analytics or admin dashboards where freshness is critical and query frequency is lower, computing aggregates dynamically with `.annotate()` is appropriate. The admin dashboard currently uses this approach for sentiment breakdown statistics.

---

### Q14. How does the watchlist toggle work with AJAX?

**Answer:**

`AddToWatchlistView` supports both standard form POST and AJAX requests using the same endpoint. It detects the request type by checking the `X-Requested-With` HTTP header:

```python
if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    return JsonResponse({'status': 'ok', 'in_watchlist': in_watchlist, 'message': message})
messages.success(request, message)
return redirect('movies:detail', pk=pk)
```

The toggle logic uses `get_or_create`:
```python
watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
if not created:
    watchlist_item.delete()
    in_watchlist = False
else:
    in_watchlist = True
```

`get_or_create` is atomic at the database level (it uses `INSERT OR IGNORE` / `SELECT` under the hood), so race conditions between clicking "add" twice are handled correctly — the second call either gets the existing record and deletes it, or creates a new one.

On the client side, vanilla JavaScript sends a `fetch` POST request with the CSRF token in the headers. On receiving the JSON response, it updates the button text and CSS class without a page reload. This provides instant feedback without the flicker of a full page navigation.

---

### Q15. Why is Naive Bayes considered "naive," and why does it still work well for text classification?

**Answer:**

Naive Bayes is "naive" because it makes the strong assumption of **conditional independence**: given the class label, each feature (word) is assumed to be independent of all other features. In reality, words are highly correlated — "not good" has a very different meaning from "not" and "good" independently — so this assumption is blatantly violated by real text.

Despite this, Naive Bayes performs surprisingly well for text classification for several reasons:

1. **Classification only needs to rank classes:** Even if the probability estimates are wrong in absolute terms, as long as the correct class has a higher probability than the incorrect one, classification is correct. The independence assumption distorts the probability magnitudes but often preserves the relative ordering.

2. **Text features are somewhat sparse:** Many words appear in only one class overwhelmingly. For movie sentiment, words like "terrible" and "masterpiece" are strong class indicators, and their conditional probabilities dominate the prediction regardless of the independence violation.

3. **Large training data compensates:** With 50,000 IMDB reviews, the individual word probability estimates are very well-calibrated even if the joint assumptions are wrong.

4. **Computational efficiency:** NB is O(n) in the number of training examples and O(k) per prediction (k = vocabulary size). It trains in seconds on the IMDB dataset and makes predictions in microseconds, which is ideal for a web application that must classify every review submission.

In NextReel, bigrams (`ngram_range=(1, 2)`) partially address the independence problem by treating "not good" as a single feature rather than two separate features.

---

### Q16. What would you change about the project if you had more time?

**Answer:**

Several improvements are clearly identified:

**Highest priority — Technical debt:**
1. Move SVD retraining to a Celery background task to avoid blocking the web request on the 50th review.
2. Wrap the review creation's database insert in a `try/except IntegrityError` to handle rare race conditions gracefully.
3. Implement proper train/test evaluation for SVD (Precision@K, Recall@K, NDCG@K) rather than just training RMSE.

**Medium priority — Feature enhancement:**
4. Integrate the TMDB API for automatic poster images, cast, crew, and trailers. The current system has no automated way to populate poster images.
5. Replace the Naive Bayes classifier with a fine-tuned DistilBERT model to significantly improve sentiment accuracy, especially for sarcasm.
6. Add a content-based filtering layer using TF-IDF on movie descriptions and combine it with SVD in a hybrid system to better handle the cold-start period.

**Lower priority — UX and scalability:**
7. Add "Why was this recommended?" explanations.
8. Migrate from SQLite to PostgreSQL for concurrent write support.
9. Implement mobile-responsive layout optimizations.
10. Add a Redis-based caching layer for recommendation results and frequent queries.

---

### Q17. How do you prevent a user from accessing another user's data or performing actions on their behalf?

**Answer:**

NextReel implements several layers of authorization:

1. **Session-based authentication:** Django sessions bind requests to a specific authenticated user. There is no way to manipulate session data from the client side (session ID is a cryptographically random token; session data is stored server-side in the database).

2. **LoginRequiredMixin / admin_required:** Views that require authentication use `LoginRequiredMixin` (for CBVs) or the `admin_required` decorator. Unauthenticated requests are redirected to the login page.

3. **Object-level ownership checks:** `DeleteReviewView` explicitly checks `review.user != request.user and not request.user.is_staff`. Only the review owner or a staff member can delete. For watchlist and watch history, Django's ORM filter (`Watchlist.objects.filter(user=request.user, movie=movie)`) ensures users can only see and modify their own records.

4. **CSRF protection:** All POST forms include Django's CSRF token. This prevents a malicious website from submitting a form on the user's behalf (cross-site request forgery).

5. **Admin guards:** The `ToggleUserActiveView` prevents a staff user from deactivating themselves, and prevents a non-superuser staff user from deactivating superusers.

There is no data in NextReel that is scoped to one user but accessible by URL to another — the profile page only shows the currently logged-in user's data, and there is no public user profile URL in the current implementation.

---

### Q18. Explain the MovieLens import command. How does it handle duplicate movies on re-import?

**Answer:**

The `import_movies` management command reads `movies.csv` and `ratings.csv` from the `datasets/` directory.

For each row in `movies.csv`, it:
1. Extracts the year from the title using regex `r'\((\d{4})\)'` (e.g., "Toy Story (1995)" → year=1995, title="Toy Story").
2. Looks up the average rating and total ratings count from `ratings.csv` (pre-aggregated using Pandas `groupby`).
3. Calls `Movie.objects.update_or_create(movielens_id=row['movieId'], defaults={...})`.
4. Sets genres using `movie.genres.set(genre_objs)`.

`update_or_create` deduplicates on `movielens_id` (the unique key from the MovieLens dataset). If a movie with the same `movielens_id` already exists, its fields are updated with the new values from the CSV. If it does not exist, a new Movie record is created.

`Genre.objects.get_or_create(name=genre_name)` ensures genre records are also deduplicated — the same genre name (e.g., "Action") will reuse the existing Genre record rather than creating a duplicate.

The entire import is wrapped in `transaction.atomic()`, meaning all changes are committed in a single database transaction. If the import fails midway (due to malformed data, disk full, etc.), the transaction is rolled back and the database remains consistent.

The `--limit` option is useful for testing: `--limit 100` imports only the first 100 movies, which is fast and useful for verifying the import logic without importing the full dataset.

---

### Q19. What is the difference between `select_related` and `prefetch_related` in Django?

**Answer:**

Both are ORM optimizations to avoid N+1 queries, but they work differently and are appropriate for different relationship types:

**`select_related`** (for ForeignKey and OneToOne relationships):
- Performs a SQL JOIN, fetching the related object in the same query.
- Example: `Review.objects.select_related('user', 'movie')` generates:
  `SELECT review.*, user.*, movie.* FROM review JOIN user ... JOIN movie ...`
- Use when: traversing ForeignKey or OneToOne fields where you will access the related object for every record.

**`prefetch_related`** (for ManyToMany and reverse ForeignKey relationships):
- Executes a separate query for the related objects, then joins them in Python memory.
- Example: `Movie.objects.prefetch_related('genres')` generates two queries:
  - `SELECT * FROM movie`
  - `SELECT * FROM genre JOIN movie_genres WHERE movie_id IN (1, 2, 3, ...)`
- Use when: fetching many-to-many relationships (like Movie → Genre) or reverse FK relationships (like Movie → Review.objects).

**Which to use:** `select_related` for ForeignKey (many-to-one), `prefetch_related` for ManyToMany and reverse FK (one-to-many). They can be combined: `Movie.objects.select_related(...).prefetch_related('genres')`.

In NextReel:
- `prefetch_related('genres')` is used on Movie queries where genre tags are rendered.
- `select_related('user')` and `select_related('movie')` are used on Review and Watchlist queries in the profile view to avoid per-item user and movie lookups.

---

### Q20. How does the theme system work technically?

**Answer:**

The theme system has two components: server-side storage and client-side rendering.

**Server-side storage:** The user's theme preference is stored in the `CustomUser.theme_preference` field as a string ('dark' or 'warm'). This persists across sessions and devices.

**Template rendering:** The base template reads `request.user.theme_preference` from the context and applies it as a CSS class on the `<body>` element:

```html
<body class="theme-{{ user.theme_preference }}">
```

For unauthenticated users, `theme_preference` defaults to 'dark'.

**CSS implementation:** The CSS uses custom properties (CSS variables) defined in theme-specific rule sets. The `--color-bg`, `--color-text`, `--color-accent`, etc. variables are defined differently for `.theme-dark` and `.theme-warm` on the `body` element. All other CSS rules use `var(--color-bg)` etc., so changing the body class switches the entire color palette.

**AJAX switching:** `SetThemeView` accepts a POST request with a `theme` parameter, validates it, updates `user.theme_preference`, and returns a JSON response. The client-side JavaScript immediately updates the body class without a page reload, providing instant visual feedback. The next full page load will use the server-persisted value.

**Security:** The `SetThemeView` is protected by `LoginRequiredMixin` and validates that the theme value is in `['dark', 'warm']`, returning a 400 error for invalid values.

---

### Q21. What is CSRF and how does Django protect against it?

**Answer:**

**Cross-Site Request Forgery (CSRF)** is an attack where a malicious website tricks a logged-in user's browser into submitting a request to another website where the user has an active session — without the user's knowledge. For example, a malicious page could contain:

```html
<form action="https://nextreel.com/reviews/add/5/" method="POST">
  <input name="rating" value="1">
  <input name="review_text" value="worst movie ever">
</form>
<script>document.forms[0].submit()</script>
```

If the user is logged into NextReel and visits this malicious page, the browser sends their session cookie with the request, and NextReel would process it as if the user had voluntarily submitted the form.

**Django's defense:** `CsrfViewMiddleware` requires every POST/PUT/PATCH/DELETE request to include a CSRF token — a cryptographically random value stored in the user's session and embedded in every form as a hidden field (`{% csrf_token %}`). When a request arrives, Django compares the submitted token against the session-stored token. The malicious page cannot know the token (it is origin-specific and not accessible to cross-origin JavaScript due to same-origin policy), so forged requests are rejected with a 403 Forbidden response.

In NextReel, all forms use `{% csrf_token %}`. AJAX requests (watchlist toggle, theme switch) include the token in the `X-CSRFToken` header, which is the accepted pattern for AJAX CSRF protection.

---

### Q22. How does your recommendation system handle movies that are in the database but were never rated by any user?

**Answer:**

There are two scenarios to consider:

**Scenario A: Movie has no ratings at all (avg_rating = 0.0).**

In `get_recommendations()`, candidate movies are those the current user has not yet rated. A movie that nobody has ever rated would be in the candidates list. When computing its predicted score:

```python
str_item = str(movie.movielens_id)
if str_item in item_index:
    # Has SVD item factors — use dot product prediction
    pred = global_mean + u_bias + item_bias[iidx] + np.dot(u_vec, item_factors[iidx])
else:
    # Not in SVD model — use stored avg_rating
    pred = movie.avg_rating  # This would be 0.0
```

If the movie's `movielens_id` is not in the SVD model's `item_index` (because it was never rated at training time), it falls back to `movie.avg_rating`, which would be 0.0. This means such movies would sort to the very bottom of recommendations — they would effectively not be recommended.

**Scenario B: Movie was imported with ratings from MovieLens but nobody has reviewed it on the site.**

The MovieLens ratings are not stored as `Review` records — they are only used to calculate the initial `avg_rating` and `total_ratings` during import. The SVD model trains only on actual site `Review` records. So these movies would also fall into the `avg_rating` fallback category.

**Implications:** Newly added movies suffer from the "item cold-start" problem — they won't be recommended until users start rating them. The "New Releases" section on the home page and cold-start recommendations page partially addresses this by surfacing new movies by year, independent of the SVD model.

---

### Q23. What is L2 regularization and why is it used in SVD training?

**Answer:**

L2 regularization (also called Ridge regularization or weight decay) adds a penalty term to the loss function that discourages large parameter values:

```
L = Σ (error²) + λ(||P||² + ||Q||² + b_u² + b_i²)
```

where λ = 0.02 in NextReel.

**Why it is needed:**

Without regularization, the SGD optimizer would drive latent factors and biases to very large values to perfectly fit the training ratings (overfitting). For example, if user U rated only one movie with a 5-star rating, without regularization the optimizer might assign an extremely large factor vector to both U and that movie, such that their dot product exactly equals 5. But this large vector would produce poor predictions for other movies.

With regularization, the penalty term forces factor magnitudes to remain small, which promotes generalization. The SGD update with regularization is:

```
p_u ← p_u + α(e_ui · q_i − λ · p_u)
```

The `−λ · p_u` term acts as a "friction force" that shrinks the vector toward zero at each step, unless the prediction error gradient is large enough to overcome it.

**Effect in practice:** With λ = 0.02 and a sufficient number of ratings per user and item, the model learns compact, meaningful representations. For users or items with very few ratings, the regularization keeps their factors close to zero, meaning their predicted ratings will be close to the global mean plus biases — which is a sensible fallback.

The choice of λ = 0.02 is a standard value from the collaborative filtering literature (used in the original FunkSVD implementation) and performs well empirically on the MovieLens dataset.

---

### Q24. What are the ethical implications of a movie recommendation system?

**Answer:**

Recommendation systems raise several important ethical concerns that I considered during this project:

**Filter bubble / echo chamber effect:** Collaborative filtering recommends items similar to what users already like and what similar users like. Over time, this can narrow users' exposure to a homogeneous set of movies (e.g., always recommending the same genre), reducing diversity and serendipitous discovery. In NextReel, the genre-grouped display somewhat mitigates this by showing recommendations across four different genres rather than a single ranked list.

**Popularity bias:** SVD models tend to have better-calibrated predictions for popular movies (more training data) than niche movies. This amplifies the already-popular movies and makes it harder for less-seen movies to surface, potentially harming cultural diversity in the catalog.

**Data privacy:** User ratings and watch history are personal behavioral data that reveal preferences. In NextReel, this data is stored in the database and used to train ML models. In a production system, proper data privacy policies (GDPR compliance, right to deletion, data minimization) would be essential. Deleting a user currently cascades to delete their reviews and history, supporting a basic right-to-erasure implementation.

**Transparency:** NextReel does not currently explain why it recommends specific movies. Users cannot understand or contest recommendation decisions. Adding "Why recommended?" explanations would improve transparency and user trust.

**Sentiment manipulation:** The automatic sentiment analysis labels user reviews as positive/negative. If users learn that a confident positive review affects something (which it currently does not in NextReel), it could incentivize sentiment manipulation.

These are important considerations for any deployed recommendation system and would be central concerns in a production product.

---

### Q25. If you were to deploy NextReel to production with 10,000 concurrent users, what changes would you make?

**Answer:**

The current architecture is designed for development and academic demonstration. A production deployment at scale would require significant changes:

**Infrastructure:**
1. **Database:** Replace SQLite with PostgreSQL (which supports concurrent writes, transactions, row-level locking, and full-text search).
2. **Web Server:** Replace Django's development server (`runserver`) with Gunicorn or uWSGI behind Nginx. Nginx handles static file serving, SSL termination, and load balancing.
3. **Containerization:** Package the application in Docker for reproducible deployments. Use Docker Compose or Kubernetes for orchestration.
4. **CDN:** Serve static files (CSS, JS, images) and media files (posters, avatars) through a CDN (e.g., Cloudflare, AWS CloudFront) to reduce server load and improve global latency.

**Caching:**
5. **Redis caching:** Cache recommendation results (pre-computed for each user), frequently accessed movie lists (trending, top-rated), and session data.
6. **Django's cache framework:** Cache the home page sections with a short TTL (e.g., 5 minutes) to avoid re-querying the database on every page load.

**Machine Learning:**
7. **Async retraining:** Move SVD retraining to Celery + Redis as a background task. Configure it to run on a schedule (e.g., nightly) rather than per-request trigger.
8. **Pre-computed recommendations:** At retraining time, compute and cache recommendations for all active users. The Recommendations page then reads from cache (milliseconds) rather than computing on demand.
9. **Model serving:** Consider a dedicated ML model serving framework (TorchServe, BentoML, or a simple FastAPI microservice) to isolate ML inference from the web application.

**Security:**
10. **Environment variables:** Store `SECRET_KEY`, database credentials, and API keys in environment variables (never in code).
11. **HTTPS:** Enforce HTTPS with Let's Encrypt certificates managed through Nginx.
12. **Rate limiting:** Implement rate limiting on login and review submission endpoints to prevent brute-force and spam attacks.

**Monitoring:**
13. **Error tracking:** Integrate Sentry for real-time error reporting and alerting.
14. **Application performance monitoring:** Use Django Debug Toolbar (dev) and a production APM tool (e.g., New Relic, Datadog) to identify slow queries and bottlenecks.

These changes would transform NextReel from an academic prototype into a production-grade application capable of serving tens of thousands of concurrent users reliably.
