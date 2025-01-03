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

    # Leer los datasets
    df = pd.read_csv("./CSV/peliculas_with_posters.csv")
    similarity_df = pd.read_csv("./CSV/updated_similarity_matrix.csv", index_col=0)

    # Calcular el promedio de calificaciones
    df["average_score"] = (df["critic_score"] + df["people_score"]) / 2

    # Mostrar películas más populares
    st.subheader("🎥 Películas más populares")
    popular_movies = df.sort_values(by="average_score", ascending=False).head(5)

    # Ajustar dinámicamente las columnas
    num_movies = len(popular_movies)
    cols = st.columns(min(num_movies, 5))  # Limitar a 5 columnas como máximo
    for index, (_, row) in enumerate(popular_movies.iterrows()):
        with cols[index % len(cols)]:
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
            # Botón para redirigir a los detalles de la película
            if st.button(f"Ver más sobre {row['title']}", key=f"movie_{row['Unnamed: 0']}"):
                st.session_state.current_page = "movie_details"
                st.session_state.current_movie_id = row["Unnamed: 0"]
                st.experimental_rerun()

    # Recomendaciones personalizadas
    st.subheader("🎭 Recomendaciones personalizadas para ti")

    if "user_data" in st.session_state and st.session_state.user_data is not None:
        # Leer datos de usuarios
        users = pd.read_csv("./CSV/users.csv")
        current_user = st.session_state.user_data["username"]
        user_index = users[users["username"] == current_user].index[0]

        try:
            rated_movies = eval(users.at[user_index, "rated_movies"]) if pd.notna(users.at[user_index, "rated_movies"]) else {}
        except (SyntaxError, ValueError):
            rated_movies = {}

        # Películas calificadas con alta puntuación
        high_rated_movies = [title for title, rating in rated_movies.items() if rating >= 4]

        # Generar recomendaciones basadas en similitudes
        recommendations = pd.DataFrame()
        for movie_title in high_rated_movies:
            if movie_title in similarity_df.index:
                similar_movies = similarity_df[movie_title].sort_values(ascending=False).head(10).index
                similar_movies_data = df[df["title"].isin(similar_movies)]
                recommendations = pd.concat([recommendations, similar_movies_data])

        # Eliminar duplicados y ordenar por puntuación promedio
        recommendations = recommendations.drop_duplicates().sort_values(by="average_score", ascending=False).head(5)

        # Mostrar recomendaciones
        num_recommendations = len(recommendations)
        cols = st.columns(min(num_recommendations, 5))  # Limitar a 5 columnas como máximo
        for index, (_, row) in enumerate(recommendations.iterrows()):
            with cols[index % len(cols)]:
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
                # Botón para redirigir a los detalles de la película
                if st.button(f"Ver más sobre {row['title']}", key=f"rec_movie_{row['Unnamed: 0']}"):
                    st.session_state.current_page = "movie_details"
                    st.session_state.current_movie_id = row["Unnamed: 0"]
                    st.experimental_rerun()

        if num_recommendations == 0:
            st.warning("No encontramos recomendaciones basadas en tus calificaciones.")
    else:
        st.info("Inicia sesión para obtener recomendaciones personalizadas.")
