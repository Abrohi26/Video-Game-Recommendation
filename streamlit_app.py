import streamlit as st
import pandas as pd

st.set_page_config(page_title="Game Recommender", layout="centered")


@st.cache_data
def load_data():
    # Make sure your repo has: data/games.csv
    df = pd.read_csv("data/games.csv")

    # Keep only the platforms you want to show
    df = df[df["platform"].isin(["Wii", "X360", "PS4", "PC"])].copy()

    # Clean numeric fields
    df["year_of_release"] = pd.to_numeric(df["year_of_release"], errors="coerce")
    df["critic_score"] = pd.to_numeric(df["critic_score"], errors="coerce").fillna(0)
    df["global_sales"] = pd.to_numeric(df["global_sales"], errors="coerce").fillna(0)

    return df


def recommend(df, platform, genre, era, critic_matters, sales_matters, top_n=10):
    d = df.copy()

    # Filters
    if platform != "Any":
        d = d[d["platform"] == platform]

    if genre != "Any":
        d = d[d["genre"] == genre]

    # Newer / Older cutoff (change if you want)
    if era == "Newer":
        d = d[d["year_of_release"] >= 2010]
    else:
        d = d[d["year_of_release"] < 2010]

    if d.empty:
        return d

    # Weights (simple + explainable)
    critic_w = 0.55 if critic_matters else 0.25
    sales_w = 0.45 if sales_matters else 0.25

    # Normalize to keep metrics comparable
    critic_norm = d["critic_score"] / (d["critic_score"].max() or 1)
    sales_norm = d["global_sales"] / (d["global_sales"].max() or 1)

    d["score"] = (critic_w * critic_norm) + (sales_w * sales_norm)

    # Deduplicate by name so one title doesn't show multiple times
    d = d.sort_values("score", ascending=False).drop_duplicates("name")

    return d.sort_values("score", ascending=False).head(top_n)


# ---------------- UI ----------------
df = load_data()

st.title("🎮 Video Game Recommendation Engine")
st.write("Portfolio demo: filter games and rank results using critic score + global sales.")

st.header("Quick Preferences")

platform = st.selectbox("Platform", ["Any", "Wii", "X360", "PS4", "PC"])

genre_options = ["Any"] + sorted(df["genre"].dropna().unique().tolist())
genre = st.selectbox("Genre", genre_options)

era = st.radio("Newer or Older?", ["Newer", "Older"], horizontal=True)

critic_matters = st.checkbox("Critic reviews matter", value=True)
sales_matters = st.checkbox("Sales/popularity matter", value=True)

top_n = st.slider("How many results?", 5, 25, 10)

if st.button("Recommend games"):
    recs = recommend(df, platform, genre, era, critic_matters, sales_matters, top_n=top_n)

    if recs.empty:
        st.warning("No matches found. Try 'Any' for platform/genre or switch Newer/Older.")
    else:
        st.subheader("Top Recommendations")

        # Show a clean results table
        st.dataframe(
            recs[["name", "platform", "genre", "year_of_release", "critic_score", "global_sales", "score"]],
            use_container_width=True
        )
with st.expander("📌 How ranking works (SQL-inspired)"):
    st.markdown("""


This app ranks games using **two signals**:

- **Critic Score** (quality)
- **Global Sales** (popularity)

Both are normalized to keep the weighting fair, then combined into a single score.
Duplicates are removed so one title doesn’t appear multiple times.
""")
        st.caption("Score uses normalized critic score and normalized global sales, weighted by your preferences.")

