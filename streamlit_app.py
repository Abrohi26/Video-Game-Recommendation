import streamlit as st
import pandas as pd

st.set_page_config(page_title="Game Recommender", layout="centered")

# ---------- Load data ----------
@st.cache_data
def load_data():
    # Put your CSV at: data/games.csv in your GitHub repo
    return pd.read_csv("data/games.csv")

# ---------- Helper: pick the right column name ----------
def pick_col(df, options):
    for c in options:
        if c in df.columns:
            return c
    return None

# ---------- Recommendation logic ----------
def recommend(df, platform, genre, era, critic_matters, sales_matters, top_n=10):
    name_col = pick_col(df, ["Name", "name", "Title", "title", "Game", "game"])
    platform_col = pick_col(df, ["Platform", "platform"])
    genre_col = pick_col(df, ["Genre", "genre"])
    year_col = pick_col(df, ["Year", "year", "Year_of_Release", "year_of_release", "Release_Year"])
    critic_col = pick_col(df, ["Critic_Score", "critic_score", "CriticScore", "Metascore", "Score"])
    sales_col = pick_col(df, ["Global_Sales", "global_sales", "GlobalSales", "Total_Sales", "total_sales"])

    d = df.copy()

    # --- filters ---
    if platform_col:
        d = d[d[platform_col].astype(str).str.contains(platform, case=False, na=False)]

    if genre_col:
        # "Other" means don't filter by genre
        if genre != "Other":
            d = d[d[genre_col].astype(str).str.contains(genre, case=False, na=False)]

    if year_col:
        d[year_col] = pd.to_numeric(d[year_col], errors="coerce")
        if era == "Newer":
            d = d[d[year_col] >= 2014]
        else:
            d = d[d[year_col] < 2014]

    # If filters got too strict, bail out nicely
    if len(d) == 0:
        return d, name_col, platform_col, genre_col, year_col, critic_col, sales_col

    # --- numeric cleanup ---
    if critic_col:
        d[critic_col] = pd.to_numeric(d[critic_col], errors="coerce").fillna(0)
    else:
        d["_critic_tmp"] = 0
        critic_col = "_critic_tmp"

    if sales_col:
        d[sales_col] = pd.to_numeric(d[sales_col], errors="coerce").fillna(0)
    else:
        d["_sales_tmp"] = 0
        sales_col = "_sales_tmp"

    # --- weights (simple + explainable) ---
    critic_w = 0.55 if critic_matters else 0.25
    sales_w = 0.45 if sales_matters else 0.25

    # --- normalization so one metric doesn't dominate ---
    critic_norm = d[critic_col] / (d[critic_col].max() or 1)
    sales_norm = d[sales_col] / (d[sales_col].max() or 1)

    d["score"] = (critic_w * critic_norm) + (sales_w * sales_norm)

    # --- remove duplicates by game name (optional, but helps GTA showing 3 times) ---
    if name_col:
        d = d.sort_values("score", ascending=False).drop_duplicates(name_col)

    d = d.sort_values("score", ascending=False).head(top_n)
    return d, name_col, platform_col, genre_col, year_col, critic_col, sales_col


# ---------- UI ----------
st.title("🎮 Video Game Recommendation Engine")
st.write("Pick a few preferences and I’ll rank games using critic score + popularity.")

st.header("Quick Preferences")

platform = st.selectbox("What platform do you want to play on?", ["PC", "PS4", "Xbox One", "Switch"])

genre = st.selectbox("What genre are you looking for?",
                     ["Action", "Shooter", "RPG", "Adventure", "Sports", "Strategy", "Other"])

era = st.radio("Do you want newer or older games?", ["Newer", "Older"], horizontal=True)

critic_matters = st.checkbox("Critic reviews matter to me", value=True)
sales_matters = st.checkbox("Sales/popularity matter to me", value=True)

top_n = st.slider("How many results?", 5, 25, 10)

if st.button("Recommend games"):
    df = load_data()
    recs, name_col, platform_col, genre_col, year_col, critic_col, sales_col = recommend(
        df, platform, genre, era, critic_matters, sales_matters, top_n=top_n
    )

    if len(recs) == 0:
        st.warning("No matches found. Try changing platform/genre or switching Newer/Older.")
    else:
        st.subheader("Top Recommendations")

        # Show only columns that exist
        cols_to_show = [c for c in [name_col, platform_col, genre_col, year_col, critic_col, sales_col, "score"] if c]
        cols_to_show = [c for c in cols_to_show if c in recs.columns]

        st.dataframe(recs[cols_to_show], use_container_width=True)

        st.caption("Scoring uses normalized critic score + normalized sales, weighted by your preferences.")
