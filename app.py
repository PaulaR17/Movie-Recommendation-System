import pandas as pd
import streamlit as st

# Cargar el dataset
df = pd.read_csv("./CSV/peliculas_with_posters.csv")

# Configuración de la página
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("Movie Recommender 🎬")
st.sidebar.header("Filtros")

# Filtros
search_title = st.sidebar.text_input("Buscar por título")
genre_filter = st.sidebar.multiselect("Filtrar por género", df['genre'].unique())

# Filtrar datos según los filtros aplicados
filtered_df = df.copy()
if search_title:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]
if genre_filter:
    filtered_df = filtered_df[filtered_df['genre'].isin(genre_filter)]

st.subheader(f"Resultados: {len(filtered_df)} películas encontradas")

# Mostrar películas como tarjetas
for index, row in filtered_df.iterrows():
    with st.container():
        # Tarjeta redondeada con diseño
        st.markdown(
            f"""
            <div style="
                border-radius: 15px; 
                background: #f9f9f9; 
                padding: 20px; 
                margin: 10px; 
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                display: flex;
                align-items: center;
            ">
                <div style="flex: 1;">
                    <img src="{row['poster_url']}" alt="{row['title']}" style="
                        width: 100%; 
                        height: auto; 
                        border-radius: 10px;
                    ">
                </div>
                <div style="flex: 2; margin-left: 20px;">
                    <h3 style="margin: 0;">{row['title']}</h3>
                    <p style="margin: 5px 0;">
                        <strong>Media de Ratings:</strong> {(row['critic_rating'] + row['user_rating']) / 2:.1f}/10
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
