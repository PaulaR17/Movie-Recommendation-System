import pandas as pd
import streamlit as st

df = pd.read_csv("./CSV/peliculas_with_posters.csv")#cargar el dataframe

st.set_page_config(page_title="Movie Recommender", layout="wide")#conf básica de la página
st.title("Movie Recommender 🎬") #titulo de la app
st.sidebar.header("Filtros")#barra lateral para los filtros
search_title = st.sidebar.text_input("Buscar por título") #opciones de filtros
genre_filter = st.sidebar.multiselect("Filtrar por género", df['genre'].unique())


filtered_df = df.copy()#filtrar datos según los filtros aplicados
if search_title:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]
if genre_filter:
    filtered_df = filtered_df[filtered_df['genre'].isin(genre_filter)]

st.subheader(f"Resultados: {len(filtered_df)} películas encontradas")#mostrar los resultados

for index, row in filtered_df.iterrows():#mostrar películas como tarjetas
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(row['poster_url'], use_column_width=True)
    with col2:
        st.subheader(row['title'])
        st.write(f"Género: {row['genre']}")
        st.write(f"Director: {row['director']}")
        st.write(f"Escritor: {row['writer']}")
