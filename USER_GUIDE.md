# NextReel — User Guide

Welcome to **NextReel**, your personal movie recommendation system. This guide walks you through every feature of the application, step by step. No technical knowledge is required.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Creating an Account](#2-creating-an-account)
3. [Logging In](#3-logging-in)
4. [The Home Page](#4-the-home-page)
5. [Browsing Movies](#5-browsing-movies)
6. [Searching and Filtering](#6-searching-and-filtering)
7. [Movie Detail Page](#7-movie-detail-page)
8. [Writing a Review](#8-writing-a-review)
9. [Managing Your Watchlist](#9-managing-your-watchlist)
10. [Watch History](#10-watch-history)
11. [Personalized Recommendations](#11-personalized-recommendations)
12. [Your Profile](#12-your-profile)
13. [Switching Themes](#13-switching-themes)
14. [Logging Out](#14-logging-out)
15. [Frequently Asked Questions](#15-frequently-asked-questions)

---

## 1. Getting Started

NextReel is a web application that helps you discover movies you will love. It learns your taste from the ratings you give and serves personalized recommendations using machine learning. You can also track what you want to watch, record what you have already watched, and read or write reviews.

To begin, open your web browser and navigate to the NextReel application URL (for example, `http://127.0.0.1:8000/` if running locally).

You will land on the **Home Page**, which is publicly accessible. However, to unlock personalized features such as recommendations, reviews, and your watchlist, you need to create a free account.

---

## 2. Creating an Account

1. From any page, click the **Register** or **Sign Up** link in the navigation bar.
2. Fill in the registration form:
   - **Username** — Choose a unique username (letters, numbers, and underscores are fine).
   - **Email** — Enter a valid email address.
   - **Password** — Choose a strong password (at least 8 characters).
   - **Confirm Password** — Re-enter your password to confirm it.
3. Click **Create Account**.
4. If everything is correct, you will be logged in automatically and redirected to the Home Page with a welcome message.

> **Note:** If you see error messages (e.g., "This username is already taken" or "Passwords do not match"), correct the highlighted fields and try again.

> **Tip:** Your username is how other users see you in reviews. Choose something you are comfortable displaying publicly.

---

## 3. Logging In

If you already have an account:

1. Click **Login** in the navigation bar.
2. Enter your **Username** and **Password**.
3. Click **Log In**.
4. You will be redirected to the Home Page (or the page you were trying to access before being prompted to log in).

> **Note:** If your credentials are incorrect, an error message will appear. Double-check your username and password. Passwords are case-sensitive.

> **Tip:** If you navigate to a protected page (such as the Recommendations page) while not logged in, the system will redirect you to the Login page and then return you to your intended destination after a successful login.

---

## 4. The Home Page

The Home Page (`/`) is your starting point. It is divided into three sections:

| Section | Description |
|---|---|
| **Top Rated** | Movies with the highest average ratings across all users. |
| **Trending** | Movies that have been watched the most recently. |
| **New Releases** | The most recently released movies in the database. |

Each movie card displays:
- The movie poster (or a default poster if none is available).
- The movie title and release year.
- The average star rating (out of 5).

**To view more details about a movie**, click anywhere on its card.

**To browse the full catalog**, click **Browse Movies** in the navigation bar or the "View All" link in any section.

---

## 5. Browsing Movies

The Browse page (`/movies/`) shows the complete movie catalog, displayed 20 movies per page.

### Navigating Pages

- Use the **Previous** and **Next** buttons at the bottom of the page to move between pages.
- You can also click a specific page number if shown.

### Filtering While Browsing

The left sidebar (or top filter bar, depending on your screen size) lets you filter the list without using the dedicated search page:

- **By Genre** — Click a genre name to show only movies in that category.
- **By Year Range** — Enter a starting year (e.g., 2000) and/or an ending year (e.g., 2020) to filter by release decade or period.
- **By Minimum Rating** — Set a minimum average rating (e.g., 3.5) to see only well-rated movies.

All filters can be combined. For example: Drama movies from 2010–2020 with a minimum rating of 4.0.

> **Tip:** The total number of matching movies is shown at the top of the results.

---

## 6. Searching and Filtering

The Search page (`/movies/search/`) gives you precise control over finding specific movies.

### How to Search by Title

1. Click **Search** in the navigation bar.
2. Type a word or part of a title in the **Search** box (e.g., "dark knight" or "star").
3. Press **Enter** or click the **Search** button.
4. Matching results appear below.

The search uses word-by-word matching, so typing "dark knight" will find movies containing both "dark" and "knight" in the title. The search is not case-sensitive.

### Advanced Filters

In addition to the title search, you can combine any of the following filters:

| Filter | How to Use |
|---|---|
| **Genre** | Select a genre from the dropdown menu. |
| **Year From** | Enter the earliest release year (e.g., 1990). |
| **Year To** | Enter the latest release year (e.g., 2005). |
| **Minimum Rating** | Enter a decimal value from 1.0 to 5.0 (e.g., 4.0). |

### Example Searches

- Find all **Action** movies from the **1990s** with a rating of at least **3.5**:
  - Genre: Action, Year From: 1990, Year To: 1999, Min Rating: 3.5
- Find movies with "ocean" in the title: just type "ocean" in the search box.

> **Tip:** Leave the title field empty and only use genre/year filters to explore movies in a category without searching by name.

---

## 7. Movie Detail Page

Clicking on any movie card takes you to the Movie Detail page. This page contains everything about a specific movie.

### Sections on the Detail Page

**Movie Header:**
- Poster image (large view).
- Title, release year, and genre tags.
- Average star rating and total number of ratings.
- "Add to Watchlist" / "Remove from Watchlist" button (login required).
- "Mark as Watched" button (login required).

**Tabs (below the header):**

- **Overview** — The movie's description and a list of genres.
- **Reviews** — All user reviews for this movie, showing the reviewer's username, star rating, review text, and the automatically detected sentiment (Positive, Negative, or Neutral).
- **Related Movies** — A carousel of other movies that share genres with the current movie.

### Interacting with the Detail Page

- To **add/remove from your watchlist**, click the bookmark-style button in the header. The button label updates instantly.
- To **mark as watched**, click "Mark as Watched". This records the movie in your watch history and increments its watch count.
- To **write a review**, scroll down to the Reviews tab (details in the next section).

> **Note:** You must be logged in to interact with the watchlist, watch history, and review features.

---

## 8. Writing a Review

You can write one review per movie. If you submit a new review for a movie you have already reviewed, your previous review will be updated.

### Steps to Write a Review

1. Navigate to the **Movie Detail page** for the movie you want to review.
2. Click the **Reviews** tab.
3. Scroll to the **Write a Review** form at the bottom of the reviews section.
4. Select a **star rating** from 1 to 5:
   - 1 star — Very poor
   - 2 stars — Below average
   - 3 stars — Average / decent
   - 4 stars — Good
   - 5 stars — Excellent
5. Type your **review text** in the text box. Describe your thoughts about the movie. There is no strict minimum length, but a more detailed review is more helpful to other users.
6. Click **Submit Review**.

### Automatic Sentiment Analysis

After you submit your review, NextReel automatically analyzes the text and assigns a sentiment label:

- **Positive** — Your review text sounds favourable.
- **Negative** — Your review text sounds unfavourable.
- **Neutral** — The sentiment is mixed or unclear.

This is done by a machine learning model trained on thousands of movie reviews. The label appears next to your review with a color-coded badge (green for positive, red for negative, grey for neutral).

> **Note:** The sentiment is detected automatically and may occasionally be inaccurate for short or ambiguous reviews. It does not affect your star rating.

### Updating or Deleting a Review

- **To update:** Simply submit the review form again for the same movie. Your existing review will be replaced with the new one.
- **To delete:** Click the **Delete** button on your review card (only visible to you on your own reviews).

> **Tip:** Your first review submission marks you as an "active user," which enables the personalized recommendation engine to start learning your preferences.

---

## 9. Managing Your Watchlist

The Watchlist lets you save movies you want to watch later.

### Adding a Movie to Your Watchlist

1. Go to the **Movie Detail page**.
2. Click the **Add to Watchlist** button (bookmark icon).
3. A confirmation message will appear: *"[Movie Title] added to your watchlist."*
4. The button label will change to **Remove from Watchlist**.

### Removing a Movie from Your Watchlist

1. On the **Movie Detail page**, click **Remove from Watchlist**.
2. The movie is immediately removed and the button reverts to **Add to Watchlist**.

### Viewing Your Full Watchlist

1. Click your **username** in the navigation bar to go to your Profile.
2. Your watchlist is displayed in a dedicated section, showing the 20 most recently added entries.

> **Note:** You must be logged in to use the Watchlist feature.

---

## 10. Watch History

NextReel automatically tracks movies you have marked as watched.

### Recording a Watch

1. Go to the **Movie Detail page**.
2. Click **Mark as Watched**.
3. A confirmation message appears and the movie is added to your watch history.

> **Note:** Each click creates a new history entry. If you watch the same movie multiple times, you can record it multiple times — each entry will be timestamped separately.

### Viewing Your Watch History

1. Go to your **Profile page** (click your username in the navigation bar).
2. Scroll to the **Watch History** section to see the 20 most recently watched movies with timestamps.

> **Tip:** The system uses your watch history to influence trending movie rankings across the platform.

---

## 11. Personalized Recommendations

The Recommendations page (`/recommendations/`) is where NextReel's machine learning shines.

### For New Users (Cold Start)

If you have not yet submitted any reviews, the system cannot build a personal profile for you. Instead, it shows three curated lists:

- **Trending Now** — Most-watched movies recently.
- **Top Rated** — Highest-rated movies by all users.
- **New Releases** — The most recently added movies.

These are a great starting point! Watch a few, write some reviews, and the system will soon start personalizing.

### For Active Users (Personalized SVD Recommendations)

Once you have submitted at least one review, the system uses **SVD (Singular Value Decomposition) Collaborative Filtering** to generate personalized recommendations. This technique identifies users with similar taste to yours and recommends movies they loved that you have not yet seen.

The Recommendations page shows your picks **grouped by genre** (up to 4 genre sections), with each section sorted by predicted rating. This means movies the system is most confident you will enjoy appear first.

> **Tip:** The more reviews you write, the better the recommendations become. Aim for at least 10–20 ratings across different genres for the best results.

> **Note:** The recommendation model is periodically retrained as more reviews are submitted to the platform, so your suggestions may improve over time even without additional input from you.

---

## 12. Your Profile

Your Profile page (`/users/profile/`) is your personal dashboard on NextReel.

### What Is on the Profile Page

| Section | Contents |
|---|---|
| **Profile Card** | Your avatar, username, bio, and join date. |
| **My Reviews** | The 20 most recent reviews you have written, with ratings and sentiment. |
| **My Watchlist** | The 20 most recently added watchlist entries. |
| **Watch History** | The 20 most recently recorded watches with timestamps. |
| **Stats** | Total reviews written, and a breakdown of positive vs. negative sentiment. |

### Editing Your Profile

1. Click **Edit Profile** on your Profile page.
2. You can update:
   - **Bio** — A short description about yourself.
   - **Avatar** — Upload a profile picture (JPG, PNG, GIF supported).
   - **Theme Preference** — Choose between Cinematic Dark and Warm Glow themes.
3. Click **Save Changes**.
4. You will be redirected back to your Profile with a success message.

> **Tip:** Your avatar and bio appear alongside your reviews on movie pages, so other users can see them.

---

## 13. Switching Themes

NextReel offers two visual themes to suit your preference:

| Theme | Description |
|---|---|
| **Cinematic Dark** (default) | A sleek dark interface inspired by cinema and streaming platforms. Deep blacks and gold accents. |
| **Warm Glow** | A softer, warmer color palette with amber and cream tones. Easier on the eyes in bright environments. |

### How to Switch Themes

**Method 1 — From the Profile Edit page:**
1. Go to **Edit Profile**.
2. Under **Theme Preference**, select your preferred option.
3. Click **Save Changes**.

**Method 2 — Quick toggle (if available in the navigation bar):**
1. Look for the theme toggle icon (sun/moon icon) in the navigation bar.
2. Click it to switch between Dark and Warm themes instantly.

Your preference is saved to your account, so it persists across sessions and devices.

> **Note:** Theme changes take effect immediately after saving.

---

## 14. Logging Out

To securely log out of NextReel:

1. Click your **username** or the **Logout** link in the navigation bar.
2. You will be logged out immediately and redirected to the Home Page.
3. A message will confirm: *"You have been logged out."*

> **Tip:** Always log out when using a shared or public computer to protect your account.

---

## 15. Frequently Asked Questions

**Q: Do I need an account to browse movies?**
A: No. You can browse the movie catalog, view detail pages, and read reviews without an account. However, you need to register to write reviews, use the watchlist, track your watch history, and receive personalized recommendations.

**Q: Why are my recommendations the same as the trending/top-rated lists?**
A: This happens when you have not yet written any reviews. The system needs your ratings to learn your preferences. Write reviews for movies you have seen and your recommendations will become personalized.

**Q: Can I review the same movie twice?**
A: No. You can only have one review per movie. If you submit a new review for a movie you have already reviewed, it will replace (update) your previous review.

**Q: Why does the sentiment label on my review seem wrong?**
A: The sentiment analysis is performed by a machine learning model trained on general movie reviews. It may occasionally misclassify short, sarcastic, or ambiguous text. The label is purely informational and does not affect your rating or how recommendations work.

**Q: How is the average rating for a movie calculated?**
A: The average rating is calculated from all user reviews submitted for that movie. It updates automatically every time a review is added, updated, or deleted.

**Q: Can I delete my watchlist entries?**
A: Yes. Go to the Movie Detail page for any movie in your watchlist and click **Remove from Watchlist**.

**Q: How often are recommendations updated?**
A: The recommendation model is automatically retrained every time 50 new reviews are submitted across the entire platform. Your individual recommendations also update the next time you visit the Recommendations page after a retraining.

**Q: Is my data private?**
A: Your reviews and star ratings are visible to all users (as they appear on movie pages). Your watchlist and watch history are private and only visible on your own Profile page.
