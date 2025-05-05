# 🎛️ Information Dashboard

A Django‐powered, single‐page dashboard that aggregates:
- **Recent Games** (past 30 days via IGDB)
- **Movies In Theaters & Upcoming** (via TMDB)
- **Tech & General News** (via NewsAPI)

All sections use responsive Bootstrap 5 card grids and share a common navbar.

---

## 🔍 What It Does

1. **Games**  
   - Fetches IGDB data using Twitch OAuth client ID & token  
   - Filters games with `first_release_date` in the last 30 days  
   - Displays cover art, title, release date  
   - “View All” page shows paginated list & detail pages  

2. **Movies**  
   - Uses TMDB’s “now_playing” and “upcoming” endpoints  
   - Shows poster, title, release date  
   - Paginated list & detail views with overview, runtime, rating  

3. **News**  
   - Pulls top headlines from NewsAPI (technology & general)  
   - Renders cards with image, title (linking out), description, source, date  

4. **Navigation**  
   - Collapsible Bootstrap navbar links to Home, Games, Movies, News  
   - Dropdown under “News” for Tech vs Top News  

---

## 🏗️ How It Works

- **`services.py`**  
  - `fetch_recent_games(days=30)`: IGDB /games query → JSON → add `cover_url`  
  - `fetch_now_playing_movies(limit)`, `fetch_upcoming_movies(limit)`: TMDB calls → add `poster_url`  
  - `fetch_tech_news(limit)`, `fetch_general_news(limit)`: NewsAPI calls  

- **`views.py`**  
  - `DashboardView`: populates context with 6 games, 8 movies, 6 news articles  
  - `GameListView` / `MovieListView` / `NewsListView`: paginated lists (12 items/page)  
  - `GameDetailView` / `MovieDetailView`: fetches single‐item details  

- **Templates (Bootstrap 5 + custom CSS)**  
  - `base.html`: `<head>` + navbar + `{% block content %}`  
  - `dashboard.html`: grid sections for Games, Movies, News  
  - `*_list.html`: paginated card grids with `<nav class="pagination">`  
  - `*_detail.html`: larger card or layout showing all metadata  

- **Static Assets**  
  - **CSS**: `static/board/css/dashboard.css` for card sizing, hover effects, typography  
  - **Images**: `static/board/img/favicon.png` for favicon/logo  

---

## 🛠️ Tech Stack & Layout

| Layer       | Technology           |
| ----------- | -------------------- |
| Backend     | Python 3.10, Django 5.x |
| Frontend    | Bootstrap 5, custom CSS |
| APIs        | IGDB (via Twitch), TMDB, NewsAPI |
| Server      | Gunicorn             |
| Hosting     | Heroku               |