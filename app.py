import streamlit as st
import pandas as pd

# Imagen de cabecera
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://via.placeholder.com/1200x300.png?text=Welcome+to+Movie+Recommender" 
             alt="Movie Recommender Header" style="width: 100%; border-radius: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Botón de cierre de sesión
col1, col2 = st.columns([9, 1])
with col2:
    if st.button("Cerrar sesión", key="logout"):
        st.session_state.current_page = "login"
        st.session_state.user_data = None

# Leer el archivo peliculas_with_posters.csv
df = pd.read_csv("./CSV/peliculas_with_posters.csv")

# Validar columnas necesarias
if 'critic_score' in df.columns and 'people_score' in df.columns and 'poster_url' in df.columns:
    # Convertir critic_score y people_score a numéricos
    df['critic_score'] = pd.to_numeric(df['critic_score'], errors='coerce')
    df['people_score'] = pd.to_numeric(df['people_score'], errors='coerce')

    # Calcular la media entre critic_score y people_score
    df['average_score'] = (df['critic_score'] + df['people_score']) / 2

    # Eliminar filas con valores nulos en average_score o poster_url
    df = df.dropna(subset=['average_score', 'poster_url'])

    # Ordenar por la media en orden descendente y seleccionar las 5 mejores
    popular_movies = df.sort_values(by="average_score", ascending=False).head(5)

    # Mostrar las películas más populares como tarjetas pequeñas
    st.subheader("🎥 Películas más populares")
    cols = st.columns(5)  # 5 columnas para mostrar 5 películas
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
else:
    st.error("El archivo CSV no contiene las columnas necesarias.")
