import streamlit as st
import pandas as pd
import ast

def parse_rated_movies(rated_movies_str):
    """
    Convert a string like '{78: 3, 352: 2, 1: 5}' into a Python dict, e.g. {78: 3, 352: 2, 1: 5}.
    """
    if pd.isna(rated_movies_str) or rated_movies_str.strip() == "":
        return {}
    return ast.literal_eval(rated_movies_str)

def get_top_similar(matrix_df, movie_id, n=3):
    """
    Returns the top-n *other* movie IDs most similar to 'movie_id'
    (i.e., excluding the movie itself),
    based on a square similarity matrix DataFrame with rows/columns = movie IDs.
    """
    if movie_id not in matrix_df.index:
        return []

    # 1) Get the row for movie_id
    row_series = matrix_df.loc[movie_id]
    # 2) Sort by descending similarity
    sorted_sim = row_series.sort_values(ascending=False)
    # 3) Exclude the movie itself
    if movie_id in sorted_sim.index:
        sorted_sim = sorted_sim.drop(movie_id)
    # 4) Take the top n
    return sorted_sim.head(n).index.tolist()

def run_app():
    # 1) Check if user is logged in
    user_data = st.session_state.get("user_data", None)
    if user_data is None:
        st.error("No hay un usuario conectado. Por favor inicie sesión primero.")
        st.stop()

    st.title("Recomendaciones de Películas")

    # 2) Load the similarity matrix
    matrix_df = pd.read_csv("./CSV/cleaned_similarity_matrix_new.csv", index_col="id")

    # 3) Load the movie details CSV
    movies_df = pd.read_csv("./CSV/peliculas_with_posters.csv")
    # Make sure 'id' is int (strip whitespace just in case)
    movies_df["id"] = movies_df["id"].astype(str).str.strip().astype(int)

    # 4) Parse user's rated movies
    rated_dict = parse_rated_movies(user_data["rated_movies"])
    # Filter for ratings > 3
    movies_above_3 = [m_id for m_id, rating in rated_dict.items() if rating > 3]

    # 5) Show the user’s info
    username = user_data["username"]
    st.markdown(f"### Usuario conectado: **{username}**")

    if not movies_above_3:
        st.write("No has valorado películas con puntuación mayor a 3.")
        return

    st.write(f"Has valorado con más de 3 las siguientes películas (IDs): {movies_above_3}")

    # 6) For each movie rated above 3, get top-3 recommended
    for m_id in movies_above_3:
        top_similar_ids = get_top_similar(matrix_df, m_id, 3)

        # Heading for this block of recommendations
        st.subheader(f"Recomendaciones para la Película con ID {m_id}:")

        # 7) Show each recommended movie in a nice layout
        for rec_id in top_similar_ids:
            # Make sure rec_id is an integer
            rec_id_int = int(rec_id)  # if needed

            # Lookup this ID in peliculas_with_posters.csv
            movie_info = movies_df[movies_df["id"] == rec_id_int]
            if movie_info.empty:
                st.write(f"- ID: {rec_id_int} (No se encontró información)")
                continue

            # Extract fields
            title = movie_info["title"].values[0]
            genre = movie_info["genre"].values[0]
            avg_score = movie_info["average_score"].values[0]
            poster_url = movie_info["poster_url"].values[0]

            # 8) Display in a "beautiful" style using HTML + st.markdown
            #    (You can tweak the styles as you wish.)
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 8px;
            ">
                <img src="{poster_url}" style="width: 120px; height: auto; border-radius: 5px;" />
                <div>
                    <h3 style="margin-bottom: 5px;">{title}</h3>
                    <p style="margin: 0;"><b>ID:</b> {rec_id_int}</p>
                    <p style="margin: 0;"><b>Género:</b> {genre}</p>
                    <p style="margin: 0;"><b>Puntuación promedio:</b> {avg_score}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("---")

# If running directly via "streamlit run app.py"
if __name__ == "__main__":
    run_app()
