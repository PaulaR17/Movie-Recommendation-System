import streamlit as st
import pandas as pd
import ast


#utilidades varias
def load_users():
    return pd.read_csv("./CSV/users.csv") #cargamos los usuarios en el dataframe

def save_users(users_df):
    users_df.to_csv("./CSV/users.csv", index=False) #guardamos el dataframe updateado

def parse_rated_movies(rated_movies_str): #para convertir los strings en un diccionario
    if pd.isna(rated_movies_str) or rated_movies_str.strip() == "":
        return {}
    return ast.literal_eval(rated_movies_str)

def serialize_rated_movies(rated_dict):
    return str(rated_dict) #hacemos la conversion inversa de diccionario a string

def get_top_similar(matrix_df, movie_id, n=3):
    """
    Nos devolverá la top-n peliculas más similares al id de las peliculas que le gustan al usuario de la matriz de similitudes
    """
    if movie_id not in matrix_df.index: #si la pelicula no esta en la matriz devuelve nada
        return []

    # 1)linea de la movie id
    row_series = matrix_df.loc[movie_id]
    # 2)lo ordena
    sorted_sim = row_series.sort_values(ascending=False)
    # 3)saca a la pelicula misma
    if movie_id in sorted_sim.index:
        sorted_sim = sorted_sim.drop(movie_id)
    # 4)agarra las 3 mejores
    return sorted_sim.head(n).index.tolist()

#para mostrar las pelis bonicas
def show_movie_card(row):
    """
    Recibe un 'row' de movies_df con columnas:
    id, title, genre, average_score, poster_url, total_ratings, popularity, etc.
    Y lo muestra con cierto estilo.
    """
    title = row.get("title", "Sin Título")
    genre = row.get("genre", "Desconocido")
    avg_score = row.get("average_score", None)
    poster_url = row.get("poster_url", None)
    total_ratings = row.get("total_ratings", None)
    #construimos un bloque HTML (usa CSS inline para estilo)
    html_block = f"""
    <div style="
        display: flex;
        flex-direction: row;
        align-items: center;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    ">
        <img src="{poster_url}" style="width: 100px; height: auto; border-radius: 5px; margin-right: 15px;" />
        <div>
            <h4 style="margin-bottom: 5px;">{title}</h4>
            <p style="margin: 0;">Género: {genre}</p>
    """

    #agrega average_score si existe
    if pd.notna(avg_score):
        html_block += f"<p style='margin: 0;'>Puntuación promedio: {avg_score}</p>"

    #agrega total_ratings si existe
    if pd.notna(total_ratings):
        html_block += f"<p style='margin: 0;'>Reseñas totales: {total_ratings}</p>"

    html_block += "</div></div>"
    st.markdown(html_block, unsafe_allow_html=True)

#funcion general
def run_app():
    # 1)mira si el usuario esta logueado
    user_data = st.session_state.get("user_data", None)
    if user_data is None:
        st.error("No hay un usuario conectado. Por favor inicie sesión primero.")
        st.stop()
    st.markdown(
        """
        <style>
        /* Cambia el color y la alineación del título principal */
        h1 {
            color: #FF5733; /* Un rojo-anaranjado llamativo */
            text-align: center;
        }
        /* Botón de cierre de sesión en la barra lateral */
        .sidebar .stButton > button {
            background-color: #d9534f !important; /* rojo bootstrap */
            color: white !important;
            border-radius: 5px !important;
        }
        .sidebar .stButton > button:hover {
            background-color: #c9302c !important; /* un rojo más oscuro */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.title("¡Recomendador de películas!")

    # 2)carga el dataframe
    # 2A)similarity Matrix (para recomendaciones)
    matrix_df = pd.read_csv("./CSV/cleaned_similarity_matrix_new.csv", index_col="id")
    # 2B)películas con sus datos (titulo, genero, etc.)
    movies_df = pd.read_csv("./CSV/peliculas_with_posters.csv")
    #aseguramos que 'id' sea int (quita espacios, por si acaso) esto ha dado una de problemas...
    movies_df["id"] = (
        movies_df["id"].astype(str).str.strip().astype(int)
    )
    # 2C)cargar usuarios (para actualizar luego los rated_movies)
    users_df = load_users()
    # 3)extraer info del usuario actual
    username = user_data["username"]

    #logica del boton de desconexion
    st.sidebar.title("Opciones")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["user_data"] = None
        st.session_state["current_page"] = "login"
        st.stop()

    # 4)secciones extra

    # 4.1)películas más populares, con más ratings
    st.subheader("Películas más populares")
    if "total_ratings" in movies_df.columns:
        top_popular = movies_df.sort_values(by="total_ratings", ascending=False).head(5)
        for idx, row in top_popular.iterrows():
            show_movie_card(row)
    else:
        st.write("No se encontró la columna 'total_ratings' para mostrar popularidad.")

    st.write("---")

    # 4.2)películas mejor valoradas, con el average score más alto
    st.subheader("Películas mejor valoradas")
    if "average_score" in movies_df.columns:
        top_rated = movies_df.sort_values(by="average_score", ascending=False).head(5)
        for idx, row in top_rated.iterrows():
            show_movie_card(row)
    else:
        st.write("No se encontró la columna 'average_score' para mostrar mejores valoraciones.")

    st.write("---")

    # 4.3)recomendaciones según tus géneros favoritos, las peliculas mejor valoradas del género que le gusta al user
    st.subheader("Recomendaciones según tus géneros favoritos")
    if pd.notna(user_data["preferences"]):
        user_genres = [g.strip() for g in user_data["preferences"].split(",") if g.strip()]
        if user_genres:
            recommended_by_genre = movies_df[movies_df["genre"].apply(lambda g:any(ug in str(g) for ug in user_genres))]
            recommended_by_genre = recommended_by_genre.sort_values(by="average_score", ascending=False).head(5)
            if not recommended_by_genre.empty:
                for idx, row in recommended_by_genre.iterrows():
                    show_movie_card(row)
            else:
                st.write("No se encontraron películas que coincidan con tus géneros favoritos.")
        else:
            st.write("No hay géneros favoritos registrados para el usuario.")
    else:
        st.write("No hay géneros favoritos registrados para el usuario.")

    st.write("---")

    # 4.4)recomendaciones personalizadas según películas que el usuario valoró con > 3
    st.subheader("Recomendaciones según tus puntuaciones")

    #parsear rated_movies del usuario actual
    rated_str = user_data.get("rated_movies", "")
    rated_dict = parse_rated_movies(rated_str)
    movies_above_3 = [m_id for m_id, rating in rated_dict.items() if rating > 3]

    if not movies_above_3:
        st.write("No has valorado películas con puntuación mayor a 3.")
    else:
        #recolectar todas las recomendaciones (top-3 por cada movie >3) en un set para evitar duplicados
        all_recommended_ids = set()

        for m_id in movies_above_3:
            top_similar_ids = get_top_similar(matrix_df, m_id, n=3)
            all_recommended_ids.update(top_similar_ids)

        if not all_recommended_ids:
            st.write("No hay recomendaciones basadas en tus valoraciones.")
        else:
            #convertir ID a int para comparar con movies_df["id"]
            all_recommended_ids_int = [int(x) for x in all_recommended_ids]

            #filtrar en movies_df
            recommended_movies_df = movies_df[movies_df["id"].isin(all_recommended_ids_int)]

            #para ordenarlas, p.ej. por average_score desc
            recommended_movies_df = recommended_movies_df.sort_values(by="average_score", ascending=False)

            for idx, row in recommended_movies_df.iterrows():
                show_movie_card(row)

    st.write("---")

    # 4.5)para calificar una película
    st.subheader("Califica una película")
    all_titles = movies_df["title"].tolist()
    selected_title = st.selectbox("Elige una película para calificar", all_titles)
    user_rating = st.slider("Tu calificación (1-5)", 1, 5, 3)

    if st.button("Guardar Calificación"):
        selected_row = movies_df[movies_df["title"] == selected_title]
        if not selected_row.empty:
            selected_id = int(selected_row["id"].values[0])
            #actualizar rated_movies en el dict
            rated_dict[selected_id] = user_rating
            #guardar en users_df
            user_index = users_df[users_df["username"] == username].index
            if not user_index.empty:
                new_rated_str = serialize_rated_movies(rated_dict)
                users_df.loc[user_index, "rated_movies"] = new_rated_str
                save_users(users_df)
                #actualizar st.session_state
                st.session_state.user_data["rated_movies"] = new_rated_str
                st.success(f"Calificaste '{selected_title}' con un {user_rating}. ¡Guardado!")
            else:
                st.error("No se encontró al usuario en la base de datos.")
        else:
            st.error("No se encontró la película seleccionada en la base de datos.")


# ----------------------------------
if __name__ == "__main__":
    #para simular un user si es necesario
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {
            "username": "test_user",
            "password": "hashed",
            "preferences": "action,horror",
            "rated_movies": "{1: 4, 530: 5}"
        }
    run_app()
