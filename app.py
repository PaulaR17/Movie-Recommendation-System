import streamlit as st
import pandas as pd

def run_app():
    # Header de la app
    st.markdown("<h1 style='text-align: center;'>Bienvenido a Movie Recommender 🎥</h1>", unsafe_allow_html=True)

    # Botón de cerrar sesión (en la parte superior)
    if st.button("Cerrar sesión", key="logout_button"):
        st.session_state.current_page = "login"
        st.session_state.user_data = None
        st.experimental_rerun()  # Redirige directamente al login

    # Leer el dataset
    df = pd.read_csv("./CSV/peliculas_with_posters.csv")

    # Calcular el promedio de calificaciones
    df["average_score"] = (df["critic_score"] + df["people_score"]) / 2

    # Mostrar películas más populares
    st.subheader("🎥 Películas más populares")
    popular_movies = df.sort_values(by="average_score", ascending=False).head(5)

    # Ajustar dinámicamente las columnas
    num_movies = len(popular_movies)
    cols = st.columns(min(num_movies, 5))  # Limitar a 5 columnas como máximo
    for index, (_, row) in enumerate(popular_movies.iterrows()):
        with cols[index % len(cols)]:  # Evita que index se desborde
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="{row['poster_url']}" alt="{row['title']}" style="width: 80%; border-radius: 10px;">
                    <h4>{row['title']}</h4>
                    <p><strong>Media de Ratings:</strong> {row['average_score']:.1f}/10</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Recomendaciones personalizadas
    st.subheader("🎭 Recomendaciones personalizadas para ti")

    if "user_data" in st.session_state and st.session_state.user_data is not None:
        user_preferences = st.session_state.user_data["preferences"].split(",")
        user_preferences = [genre.strip().lower() for genre in user_preferences]

        df["genre"] = df["genre"].str.lower()

        recommendations = df[df["genre"].str.contains('|'.join(user_preferences), na=False)]
        recommendations = recommendations.sort_values(by="average_score", ascending=False).head(5)

        # Ajustar dinámicamente las columnas
        num_recommendations = len(recommendations)
        cols = st.columns(min(num_recommendations, 5))  # Limitar a 5 columnas como máximo
        for index, (_, row) in enumerate(recommendations.iterrows()):
            with cols[index % len(cols)]:  # Evita que index se desborde
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="{row['poster_url']}" alt="{row['title']}" style="width: 80%; border-radius: 10px;">
                        <h4>{row['title']}</h4>
                        <p><strong>Media de Ratings:</strong> {row['average_score']:.1f}/10</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        if num_recommendations == 0:
            st.warning("No encontramos recomendaciones basadas en tus preferencias.")
    else:
        st.info("Inicia sesión para obtener recomendaciones personalizadas.")
