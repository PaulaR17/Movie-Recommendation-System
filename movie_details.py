import streamlit as st
import pandas as pd

def show_movie_details():
    # Verificar si hay una película seleccionada
    movie_id = st.session_state.get("current_movie_id")
    if movie_id is None:
        st.error("No se seleccionó ninguna película.")
        st.stop()

    # Cargar el dataset
    df = pd.read_csv("./CSV/peliculas_with_posters.csv")

    # Calcular el promedio de calificaciones si no existe
    if "average_score" not in df.columns:
        df["average_score"] = (df["critic_score"] + df["people_score"]) / 2

    # Filtrar la película seleccionada
    movie = df[df["Unnamed: 0"] == movie_id].iloc[0]

    # Estilo CSS para ajustar márgenes, fuentes, y estrellas
    st.markdown(
        """
        <style>
            .movie-title {
                font-size: 32px;
                font-weight: bold;
                text-align: center;
            }
            .movie-details {
                font-size: 18px;
                margin: 5px 0;
            }
            .movie-synopsis {
                font-size: 16px;
                line-height: 1.6;
                margin: 10px 0;
            }
            .rating-section {
                font-size: 20px;
                text-align: center;
                margin-top: 20px;
            }
            .star-container {
                text-align: center;
                font-size: 30px;
                margin: 10px 0;
                color: #FFD700;
            }
            .star-container div {
                display: inline-block;
                margin: 0 auto;
            }
            .star {
                cursor: pointer;
                padding: 0 5px;
            }
            .star:hover {
                color: #FFA500;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Mostrar título de la película
    st.markdown(f"<h1 class='movie-title'>{movie['title']}</h1>", unsafe_allow_html=True)

    # Dividir en columnas para imagen y detalles
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(movie["poster_url"], width=200)  # Imagen más pequeña
    with col2:
        st.markdown(f"<p class='movie-details'><strong>Género:</strong> {movie['genre']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='movie-details'><strong>Puntuación promedio:</strong> {movie['average_score']:.1f}/10</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='movie-synopsis'><strong>Sinopsis:</strong> {movie['synopsis']}</p>", unsafe_allow_html=True)

    # Sección de calificación
    st.markdown("<div class='rating-section'>Califica esta película:</div>", unsafe_allow_html=True)

    # Sistema de estrellas centrado
    st.markdown("<div class='star-container'>", unsafe_allow_html=True)
    rating = st.radio(
        "",
        options=[1, 2, 3, 4, 5],
        index=2,  # Predeterminado en 3 estrellas
        format_func=lambda x: "★" * x + "☆" * (5 - x),
        horizontal=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Botón de enviar calificación
    if st.button("Enviar calificación", key="submit_rating"):
        update_user_rating(movie_id, rating)
        st.success(f"¡Gracias por calificar con {rating} estrellas!")
        st.experimental_rerun()

def update_user_rating(movie_id, rating):
    # Cargar el archivo de usuarios
    users = pd.read_csv("./CSV/users.csv")
    current_user = st.session_state.user_data["username"]

    # Obtener el índice del usuario actual
    user_index = users[users["username"] == current_user].index[0]

    # Manejar posibles valores nulos o vacíos en 'rated_movies'
    try:
        rated_movies = eval(users.at[user_index, "rated_movies"]) if pd.notna(users.at[user_index, "rated_movies"]) else {}
    except (SyntaxError, ValueError):
        rated_movies = {}

    # Actualizar el diccionario de calificaciones
    rated_movies[movie_id] = rating
    users.at[user_index, "rated_movies"] = str(rated_movies)

    # Guardar los cambios en el archivo CSV
    users.to_csv("./CSV/users.csv", index=False)