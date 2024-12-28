import streamlit as st
import pandas as pd

# Image header
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://via.placeholder.com/1200x300.png?text=Welcome+to+Movie+Recommender" 
             alt="Movie Recommender Header" style="width: 100%; border-radius: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Logout button
col1, col2 = st.columns([9, 1])
with col2:
    if st.button("Cerrar sesión", key="logout"):
        st.session_state.current_page = "login"
        st.session_state.user_data = None

# Read the dataset
df = pd.read_csv("./CSV/peliculas_with_posters.csv")

# Calculate the average score
df["average_score"] = (df["critic_score"] + df["people_score"]) / 2

# Display most popular movies
st.subheader("🎥 Películas más populares")
popular_movies = df.sort_values(by="average_score", ascending=False).head(5)
cols = st.columns(5)
for index, row in enumerate(popular_movies.iterrows()):
    _, row = row
    with cols[index]:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{row['poster_url']}" alt="{row['title']}" style="width: 80%; border-radius: 10px;">
                <h4 style="margin: 10px 0;">{row['title']}</h4>
                <p style="margin: 0;"><strong>Media de Ratings:</strong> {row['average_score']:.1f}/10</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Personalized Recommendations
# Personalized Recommendations
st.subheader("🎭 Recomendaciones personalizadas para ti")

# Check if user is logged in and has preferences
if "user_data" in st.session_state and st.session_state.user_data is not None:
    user_preferences = st.session_state.user_data["preferences"].split(",")
    user_preferences = [genre.strip().lower() for genre in user_preferences]  # Normalize user preferences

    # Normalize genre column in the dataset
    df["genre"] = df["genre"].str.lower()

    # Debugging info (optional)
    # st.write(f"User Preferences: {user_preferences}")  # Remove after debugging
    # st.write(f"Available Genres in Dataset: {df['genre'].unique()}")  # Remove after debugging

    # Filter for personalized recommendations
    recommendations = []
    for genre in user_preferences:
        matches = df[df["genre"].str.contains(genre, na=False)]
        recommendations.append(matches)

    # Combine and sort recommendations
    if recommendations:
        recommended_movies = pd.concat(recommendations).drop_duplicates()
        recommended_movies = recommended_movies.sort_values(by=["average_score"], ascending=False).head(5)

        # Display recommendations
        if not recommended_movies.empty:
            cols = st.columns(len(recommended_movies))
            for index, row in enumerate(recommended_movies.iterrows()):
                _, row = row
                with cols[index]:
                    st.markdown(
                        f"""
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="{row['poster_url']}" alt="{row['title']}" style="width: 80%; border-radius: 10px;">
                            <h4 style="margin: 10px 0;">{row['title']}</h4>
                            <p style="margin: 0;"><strong>Media de Ratings:</strong> {row['average_score']:.1f}/10</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.warning("No encontramos recomendaciones basadas en tus preferencias. ¡Prueba añadiendo más géneros!")
    else:
        st.warning("No encontramos recomendaciones basadas en tus preferencias. ¡Prueba añadiendo más géneros!")
else:
    st.info("Inicia sesión para obtener recomendaciones personalizadas.")
