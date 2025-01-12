import streamlit as st
import pandas as pd

def show_movie_details():
    #verificar si hay una película seleccionada
    movie_id = st.session_state.get("current_movie_id")
    if movie_id is None:
        st.error("No se seleccionó ninguna película.")
        st.stop()

    if st.button("Volver atrás", key="back_button"):
        st.session_state.current_page = "app"  #cambiar a la página principal
        st.experimental_rerun()  #recargar la página

    df = pd.read_csv("./CSV/peliculas_with_posters.csv")
    if "average_score" not in df.columns:
        df["average_score"] = (df["critic_score"] + df["people_score"]) / 2

    #filtrar la película seleccionada
    movie = df[df["Unnamed: 0"] == movie_id].iloc[0]
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
    st.markdown(f"<h1 class='movie-title'>{movie['title']}</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(movie["poster_url"], width=200)  # Imagen más pequeña
    with col2:
        st.markdown(f"<p class='movie-details'><strong>Género:</strong> {movie['genre']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='movie-details'><strong>Puntuación promedio:</strong> {movie['average_score']:.1f}/10</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='movie-synopsis'><strong>Sinopsis:</strong> {movie['synopsis']}</p>", unsafe_allow_html=True)
    st.markdown("<div class='rating-section'>Califica esta película:</div>", unsafe_allow_html=True)
    st.markdown("<div class='star-container'>", unsafe_allow_html=True)
    rating = st.radio(
        "",
        options=[1, 2, 3, 4, 5],
        index=2,
        format_func=lambda x: "★" * x + "☆" * (5 - x),
        horizontal=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Enviar calificación", key="submit_rating"):
        update_user_rating(movie_id, rating)
        st.success(f"¡Gracias por calificar con {rating} estrellas!")
        st.experimental_rerun()

def update_user_rating(movie_id, rating):
    users = pd.read_csv("./CSV/users.csv")
    current_user = st.session_state.user_data["username"]
    user_index = users[users["username"] == current_user].index[0]
    try:
        rated_movies = eval(users.at[user_index, "rated_movies"]) if pd.notna(users.at[user_index, "rated_movies"]) else {}
    except (SyntaxError, ValueError):
        rated_movies = {}
    rated_movies[movie_id] = rating
    users.at[user_index, "rated_movies"] = str(rated_movies)
    users.to_csv("./CSV/users.csv", index=False)