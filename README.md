# movie-recommender-dash-app
A movie recommendation engine built with Python Dash and TMDB API.
# 🎬 Movie Recommender Dash App

This project is a **web-based movie recommendation system** built using Python Dash and the TMDB API.  
It allows users to explore and search for movies, view detailed information about movies and actors, and experience a seamless navigation flow between pages.

---

## 🌟 Core Features

### 🏠 Home Discovery Page (`page_home_discovery.py`)
- Search movies by tag, genre, or keyword.
- Filter and sort results by rating or year.
- View a bar chart of the **Top 10 movies**.
- Paginated results for smoother browsing.

### 🎬 Movie Details Page (`page_movie_details.py`)
- Displays movie overview, release date, rating, and cast list.
- Fetches and shows poster images dynamically from TMDB.
- Interactive layout that updates based on user selection.

### 👤 Actor Details Page (`page_actor_details.py`)
- Shows actor biography, profile picture, and top 10 notable movies.
- Each movie card is clickable for quick exploration.
- Includes back navigation to return to the previous page.

---

## 🧭 Navigation and Smart Back Feature

Initially, the back button always returned to the homepage.  
After refactoring to use Dash’s `use_pages=True`, modular pages and **smart navigation** were introduced.

- `dcc.Store` keeps track of the previous page (`id="previous-page"`).  
- A callback in `app.py` updates this value when the URL changes.  
- `navigation_back_handler.js` handles browser-based back navigation for a native experience.

---

## ⚙️ Code Structure

> The project is modularly organized for clarity and scalability:

- **app.py** — Main app file and navigation controller  
- **movie_data_loader.py** — Loads and processes movie dataset  
- **utils.py** — Shared helper functions and TMDB API calls  
- **pages/**  
  - `page_home_discovery.py` — Home discovery and search page  
  - `page_movie_details.py` — Movie detail view  
  - `page_actor_details.py` — Actor detail view  
- **assets/** — Static files (CSS, icons)  
- **navigation_back_handler.js** — JavaScript for smart back button logic  
- **requirements.txt** — List of dependencies  
- **Movie_Recommender’s_Report.pdf** — Final project report

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/tolulopeoluwabunmi/movie-recommender-dash-app.git

# Navigate into the project directory
cd movie-recommender-dash-app

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
