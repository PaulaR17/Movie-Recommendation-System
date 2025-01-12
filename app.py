import streamlit as st
import pandas as pd

def run_app():
    # Cargar datos
    peliculas_path = './CSV/peliculas_with_posters.csv'
    user_db_path = './CSV/users.csv'
    similarity_matrix_path = './CSV/cleaned_similarity_matrix.csv'

    peliculas_df = pd.read_csv(peliculas_path)
    peliculas_df.reset_index(inplace=True)  # Añadimos un índice numérico único
    peliculas_df["title_normalized"] = peliculas_df["title"].str.strip().str.lower()

    users_df = pd.read_csv(user_db_path)

    similarity_matrix_df = pd.read_csv(similarity_matrix_path).set_index('id')

    # Asegurar que los índices en la matriz de similitud sean cadenas
    similarity_matrix_df.index = similarity_matrix_df.index.astype(str)
    similarity_matrix_df.columns = similarity_matrix_df.columns.astype(str)

    # Convertir todos los valores de la matriz de similitud a tipo float, manejando errores
    similarity_matrix_df = similarity_matrix_df.apply(pd.to_numeric, errors='coerce')

    # Eliminar filas y columnas completamente vacías o no numéricas
    similarity_matrix_df = similarity_matrix_df.dropna(how='all', axis=0)
    similarity_matrix_df = similarity_matrix_df.dropna(how='all', axis=1)

    # Normalizar los valores de la matriz de similitud
    if not similarity_matrix_df.empty:
        similarity_matrix_df = similarity_matrix_df / similarity_matrix_df.max().max()

    # Validar que los IDs de similarity_matrix_df estén en peliculas_df
    valid_ids = peliculas_df['id'].astype(str).tolist()
    similarity_matrix_df = similarity_matrix_df[similarity_matrix_df.index.isin(valid_ids)]
    similarity_matrix_df = similarity_matrix_df[[col for col in similarity_matrix_df.columns if col in valid_ids]]

    # Obtener el usuario actual desde el estado de sesión
    current_user = st.session_state.get("user_data", {})

    st.title("Películas Recomendadas 🎥")

    # Función para guardar puntuaciones
    def guardar_puntuacion(index, puntuacion):
        if "rated_movies" not in current_user or pd.isna(current_user["rated_movies"]):
            rated_movies = {}
        else:
            rated_movies = eval(current_user["rated_movies"])

        rated_movies[index] = puntuacion
        current_user["rated_movies"] = str(rated_movies)

        # Guardar en el CSV
        user_row = users_df[users_df["username"] == current_user["username"]]
        if not user_row.empty:
            users_df.loc[user_row.index, "rated_movies"] = current_user["rated_movies"]
            users_df.to_csv(user_db_path, index=False)
            st.success(f"Puntuación de {puntuacion} estrellas guardada para la película con índice {index}.")
        else:
            st.error("No se pudo guardar la puntuación en el archivo de usuarios.")

    # Función para obtener recomendaciones basadas en puntuaciones
    def obtener_recomendaciones():
        if "rated_movies" not in current_user or pd.isna(current_user["rated_movies"]):
            return []

        rated_movies = eval(current_user["rated_movies"])
        recomendaciones = {}

        for pelicula_id in similarity_matrix_df.index:
            if pelicula_id not in rated_movies:
                similitudes = similarity_matrix_df.loc[pelicula_id]
                puntuacion_acumulada = sum(
                    float(rated_movies.get(str(rated_pelicula), 0)) * similitud
                    for rated_pelicula, similitud in similitudes.items()
                    if str(rated_pelicula) in rated_movies and similitud > 0.7
                )
                if puntuacion_acumulada > 0:
                    recomendaciones[pelicula_id] = puntuacion_acumulada

        recomendaciones_ordenadas = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
        valid_recommendations = [rec[0] for rec in recomendaciones_ordenadas if rec[0] in peliculas_df['id'].astype(str).values]
        return valid_recommendations

    # Sección: Mejor puntuadas
    st.header("Mejor puntuadas")
    mejor_puntuadas = peliculas_df.sort_values(by="average_score", ascending=False).head(10)
    for idx, row in mejor_puntuadas.iterrows():
        col1, col2, col3 = st.columns([1, 4, 2])
        with col1:
            st.image(row["poster_url"], width=100)
        with col2:
            st.subheader(row["title"])
            st.write(f"Puntuación media: {row['average_score']}")
            st.write(f"Sinopsis: {row['synopsis'][:200]}...")
        with col3:
            puntuacion = st.slider(f"Puntúa '{row['title']}'", 0, 5, 0, key=f"rating_{row['id']}_{idx}")
            if st.button("Guardar", key=f"save_{row['id']}_{idx}"):
                guardar_puntuacion(row['index'], puntuacion)

    # Sección: Más populares
    st.header("Más populares")
    populares = peliculas_df.sort_values(by="total_reviews", ascending=False).head(10)
    for idx, row in populares.iterrows():
        col1, col2, col3 = st.columns([1, 4, 2])
        with col1:
            st.image(row["poster_url"], width=100)
        with col2:
            st.subheader(row["title"])
            st.write(f"Total de reseñas: {row['total_reviews']}")
            st.write(f"Sinopsis: {row['synopsis'][:200]}...")
        with col3:
            puntuacion = st.slider(f"Puntúa '{row['title']}'", 0, 5, 0, key=f"rating_{row['title']}_{idx}")
            if st.button("Guardar", key=f"save_{row['title']}_{idx}"):
                guardar_puntuacion(row['id'], puntuacion)

    # Sección: Recomendaciones por género
    if "preferences" in current_user:
        user_preferences = current_user["preferences"].split(',')
        st.header("Recomendaciones según tus géneros favoritos")
        recomendaciones_genero = peliculas_df[peliculas_df["genre"].isin(user_preferences)].sort_values(by="average_score", ascending=False).head(10)

        if not recomendaciones_genero.empty:
            for _, row in recomendaciones_genero.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(row["poster_url"], width=100)
                with col2:
                    st.subheader(row["title"])
                    st.write(f"Puntuación media: {row['average_score']}")
                    st.write(f"Género: {row['genre']}")
                    st.write(f"Sinopsis: {row['synopsis'][:200]}...")

    # Sección: Recomendaciones basadas en puntuaciones
    st.header("Recomendaciones según tus puntuaciones")
    recomendaciones = obtener_recomendaciones()
    if recomendaciones:
        peliculas_df['id'] = peliculas_df['id'].astype(str)  # Asegurar que las IDs son del mismo tipo
        recomendadas_df = peliculas_df[peliculas_df['id'].isin(recomendaciones)]

        if not recomendadas_df.empty:
            for _, row in recomendadas_df.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(row["poster_url"], width=100)
                with col2:
                    st.subheader(row["title"])
                    st.write(f"Puntuación media: {row['average_score']}")
                    st.write(f"Sinopsis: {row['synopsis'][:200]}...")
        else:
            st.write("No se encontraron películas recomendadas en el DataFrame.")
    else:
        st.write("No hay recomendaciones basadas en tus puntuaciones todavía. Puntúa más películas para obtener mejores resultados.")

    # Botón para cerrar sesión
    st.sidebar.title("Opciones")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.current_page = "login"
        st.session_state.user_data = None
        st.stop()

if __name__ == "__main__":
    run_app()
