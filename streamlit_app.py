import streamlit as st
import pandas as pd

st.set_page_config(page_title="Game Recommender", layout="centered")

@st.cache_data
def load_data():
    return pd.read_csv("data/games.csv")

def recommend(df, platform, genre, era, critic_matters, sales_matters, top_n=10):
    d = df.copy()

    # Filters
    if platform != "Any":
        d = d[d["platform"] == platform]

    if genre != "Any":
        d = d[d["genre"] == genre]

    # Year filter
    d["year_of_release"] = pd.to_numeric(d["year_of_release"], errors="coerce")

    if era == "Newer":
        d = d[d["year_of_release"] >= 2010]
    else:
        d = d[d["year_of_release"] < 2010]

    if len(d) == 0:
        return d

    # Numeric cleanup
    d["critic_score"] = pd.to_numeric(d["critic_score"], errors="coerce").fillna(0)
    d["global_sales"] = pd.to_numeric(d["global_sales"], errors="coerce").fillna(0)

    # Weights
    critic_w = 0.55 if critic_matters else 0.25
    sales_w  = 0.45 if sales_matters else 0.25

    # Normalize
    critic_norm = d["critic_score"] / (d["critic_score"].max() or 1)
    sales_norm  = d["global_sales"] / (d["global_sales"].max() or 1)

    d["score"] = (critic_w * critic_norm) + (sales_w * sales_norm)

    # Remove duplicates by game name (helps with repeated titles across platforms)
    d = d.sort_values("score", ascending=False).drop_duplicates("name")

    return d.sort_values("score", ascending=False).head(top_n)

# ---------------- UI ----------------
df = load_data()

st.title("🎮 Video Game Recommendation Engine")
st.write("Portfolio demo: filters + ranking using critic score and global sales.")

st.header("Quick Preferences")

allowed_platforms = ["Any", "Wii", "X360", "PS4", "PC"]
platform = st.selectbox("Platform", allowed_platforms)

platform = st.selectbox("Platform", platform_options)
genre = st.selectbox("Genre", genre_options)

era = st.radio("Newer or Older?", ["Newer", "Older"], horizontal=True)
critic_matters = st.checkbox("Critic reviews matter", value=True)
sales_matters = st.checkbox("Sales/popularity matter", value=True)

top_n = st.slider("How many results?", 5, 25, 10)

if st.button("Recommend games"):
    recs = recommend(df, platform, genre, era, critic_matters, sales_matters, top_n=top_n)

    if len(recs) == 0:
        st.warning("No matches found. Try 'Any' for platform/genre or switch Newer/Older.")
    else:
        st.subheader("Top Recommendations")
        st.dataframe(
            recs[["name", "platform", "genre", "year_of_release", "critic_score", "global_sales", "score"]],
            use_container_width=True
        )

