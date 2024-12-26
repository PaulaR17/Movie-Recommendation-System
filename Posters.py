import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Leer la API Key desde el archivo .env
API_KEY = os.getenv("API_KEY")
# Endpoint base de TMDB
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_poster(title): #obtener el poster de una peli
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title
    }
    response = requests.get(url, params=params).json()


    if response.get("results"):#si hay resultados se obtiene la priemera imagen
        poster_path = response["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"  # URL completa del poster
    return "No Poster Found"


#cargar el dataset de películas
df = pd.read_csv("CSV/peliculas.csv")
duplicates = df[df.duplicated(subset=['title'], keep=False)]
print("Duplicados encontrados:")
print(duplicates)

df = df.drop_duplicates(subset=['title'], keep='first')
#agregar la columna de URLs de posters
df['poster_url'] = df['title'].apply(get_movie_poster)

df.to_csv("./CSV/peliculas_with_posters.csv", index=False)
print("Posters obtenidos y guardados.")
