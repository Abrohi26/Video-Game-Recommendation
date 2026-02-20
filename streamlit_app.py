import streamlit as st

st.set_page_config(page_title="Game Recommender", layout="centered")

st.title("🎮 Video Game Recommendation Engine")
st.write("This is my Streamlit demo app for a portfolio project.")

st.header("Quick Preferences")

platform = st.selectbox(
    "What platform do you want to play on?",
    ["PC", "PS4", "Xbox One", "Switch"]
)

genre = st.selectbox(
    "What genre are you looking for?",
    ["Action", "Shooter", "RPG", "Adventure", "Sports", "Strategy", "Other"]
)

era = st.radio(
    "Do you want newer or older games?",
    ["Newer", "Older"],
    horizontal=True
)

critic_matters = st.checkbox("Critic reviews matter to me", value=True)
sales_matters = st.checkbox("Sales/popularity matter to me", value=True)

if st.button("Recommend games"):
    st.success("✅ App is working! Next step: connect to your dataset/SQL ranking query.")
    st.write("Your selections:")
    st.write(
        {
            "platform": platform,
            "genre": genre,
            "era": era,
            "critic_matters": critic_matters,
            "sales_matters": sales_matters,
        }
    )
