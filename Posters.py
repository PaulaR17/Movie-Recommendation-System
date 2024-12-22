import requests
import pandas as pd

# TMDB API Key
API_KEY = "91ad0c05532cf90cc3e5a3cf7b612882"

# Endpoint base de TMDB
BASE_URL = "https://api.themoviedb.org/3"


# Función para obtener el poster de una película
def get_movie_poster(title):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title
    }
    response = requests.get(url, params=params).json()

    # Verificar si hay resultados y obtener el primer poster
    if response.get("results"):
        poster_path = response["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"  # URL completa del poster
    return "No Poster Found"


# Cargar el dataset de películas
df = pd.read_csv("./CSV/peliculas.csv")

# Agregar la columna de URLs de posters
df['poster_url'] = df['title'].apply(get_movie_poster)

# Guardar el dataset actualizado
df.to_csv("./CSV/peliculas_with_posters.csv", index=False)

print("Posters obtenidos y guardados.")
