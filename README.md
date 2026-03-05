# 🎮 Video Game Recommendation Engine (Streamlit)

A portfolio project that recommends and ranks video games based on user preferences using a weighted scoring model (critic score + global sales). Deployed as a Streamlit web app for easy sharing with recruiters/hiring managers.

## Live Demo
- Streamlit App: https://lnkd.in/gXCQQQcd

- <img width="1923" height="854" alt="Video Games Recommendation" src="https://github.com/user-attachments/assets/11c473f7-ccd8-43fc-b2cb-3567da609eae" />
- <img width="1922" height="867" alt="VG 2" src="https://github.com/user-attachments/assets/34a3d45d-c904-4c7e-a87c-5d2f73ffe9ad" />
<img width="1928" height="802" alt="BG 3" src="https://github.com/user-attachments/assets/1e579b6c-4682-42f6-beae-ba744d54d87d" />


## Problem
With thousands of games across platforms and genres, it’s hard for a player to quickly find high-quality options that match their preferences. This app helps narrow choices and provides explainable ranked results.

## Data
Source dataset: (Kaggle / name if you want)
Key fields used:
- `name` — game title
- `platform` — console/PC
- `genre` — primary genre
- `year_of_release` — release year
- `critic_score` — review score (quality signal)
- `global_sales` — worldwide sales (popularity signal)


## How Recommendations Work
The app filters the dataset based on:
- Platform (Wii / X360 / PS4 / PC)
- Genre (optional)
- Newer vs older games (cutoff at 2010)

Then it ranks the remaining games using a weighted score:

**Score = w1 * normalized(critic_score) + w2 * normalized(global_sales)**

Where:
- If “Critic reviews matter” is checked → critic weight increases
- If “Sales matter” is checked → sales weight increases
- Normalization prevents either metric from dominating due to scale differences

Duplicates are removed by title so a single game doesn’t flood results across platforms.

## Tech Stack
- Python, Pandas (data filtering + scoring)
- Streamlit (UI + deployment)
- PostgreSQL / pgAdmin (original SQL exploration + cleaning workflow)
- GitHub + Streamlit Community Cloud (deployment)

## Repository Structure
- `streamlit_app.py` — Streamlit UI + recommendation logic
- `data/games.csv` — cleaned dataset snapshot for deployment
- `sql/` — SQL scripts used for exploration/cleaning (optional but recommended)
- `notebooks/` — Python EDA notebook (optional but recommended)

## What I’d Improve Next

- Add user-driven weight sliders (instead of checkboxes)
- Add platform-friendly mapping (PS4 → PlayStation 4, etc.)
- Add “similar games” recommendations using cosine similarity on genres + scores
- Add visuals: top genres, score breakdown per result

## Author
Amir Brohi (GitHub: Abrohi26)
