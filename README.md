# 🎮 Video Game Recommendation Engine

A weighted ranking engine that helps users discover high-quality video games based on personal preferences — built with PostgreSQL, Python, and deployed as an interactive Streamlit web app.

**[▶ Try the Live App](https://lnkd.in/gXCQQQcd)**

---

## Screenshots

![App Overview](https://private-user-images.githubusercontent.com/173987974/559002515-11c473f7-ccd8-43fc-b2cb-3567da609eae.PNG)

![Filtered Results](https://private-user-images.githubusercontent.com/173987974/559002553-34a3d45d-c904-4c7e-a87c-5d2f73ffe9ad.PNG)

![Scoring in Action](https://private-user-images.githubusercontent.com/173987974/559002607-1e579b6c-4682-42f6-beae-ba744d54d87d.PNG)

---

## Problem

With thousands of games across platforms and genres, players struggle to quickly identify high-quality titles that match their preferences. This app filters and ranks games using explainable, user-controlled scoring — giving clear, justified recommendations rather than a black-box result.

---

## How It Works

The app filters the dataset by platform, genre, and release era, then scores results using a normalized weighted formula:

**Score = w1 × normalized(critic_score) + w2 × normalized(global_sales)**

- Users control weighting via checkboxes ("Critic reviews matter" / "Sales matter")
- Normalization prevents either metric from dominating due to scale differences
- Duplicate titles are deduplicated across platforms so one game doesn't flood results

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data exploration & cleaning | PostgreSQL, pgAdmin |
| App logic | Python, Pandas |
| Frontend & deployment | Streamlit, Streamlit Community Cloud |
| Version control | GitHub |

---

## Data

**Source:** Kaggle — Video Game Sales dataset (16,598 games)

Key fields: `name`, `platform`, `genre`, `year_of_release`, `critic_score`, `global_sales`

---

## Repository Structure
```
├── streamlit_app.py   # App logic and UI
├── data/games.csv     # Cleaned dataset
└── sql/               # PostgreSQL scripts for EDA and cleaning
```

---

## What I'd Improve Next

- Replace checkboxes with continuous sliders for finer weight control
- Add platform-friendly display names (e.g. X360 → Xbox 360)
- Implement "similar games" feature using cosine similarity on genre + score vectors
- Add visualizations: genre distribution, score breakdown charts

---

## Author

**Amir Brohi** · [LinkedIn](https://www.linkedin.com/in/amirbrohi/) · [GitHub](https://github.com/Abrohi26)
