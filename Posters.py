import requests
import pandas as pd
import os
with open("api_key.txt", "r") as f:
    API_KEY = f.read().strip()
BASE_URL = "https://api.themoviedb.org/3"

# Diccionario para traducir géneros
GENRE_TRANSLATION = {
    "acción": "action",
    "aventura": "adventure",
    "ciencia ficción": "sci fi",
    "comedia": "comedy",
    "drama": "drama",
    "fantasía": "fantasy",
    "horror": "horror",
    "misterio": "mystery and thriller",
    "romance": "romance",
    "animación": "animation",
    "documental": "documentary",
    "musical": "musical",
    "historia": "history",
    "guerra": "war",
    "crimen": "crime",
    "infantil": "kids and family",
    "otros": "other",
    # Añade más si es necesario
}

def translate_genres(genres):
    if pd.isna(genres):
        return "Desconocido"  #reemplazar géneros nulos por 'Desconocido'
    translated_genres = []
    for genre in genres.split(", "):
        genre_lower = genre.strip().lower()
        translated_genres.append(GENRE_TRANSLATION.get(genre_lower, genre_lower))  #traduce o deja igual si no está en el diccionario
    return ", ".join(translated_genres)

def get_movie_poster(title):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title
    }
    response = requests.get(url, params=params).json()

    if response.get("results"):  #si hay resultados, toma el primer póster
        poster_path = response["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"  #URL completa del póster
    return "No Poster Found"

df = pd.read_csv("CSV/peliculas.csv")
df["genre"] = df["genre"].apply(translate_genres)

duplicates = df[df.duplicated(subset=['title'], keep=False)]
print("Duplicados encontrados:")
print(duplicates)
df = df.drop_duplicates(subset=['title'], keep='first')

#rellenar valores nulos
categorical_columns = df.select_dtypes(include="object").columns
numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns

df[categorical_columns] = df[categorical_columns].fillna("Desconocido")  #textos como 'Desconocido'
df[numerical_columns] = df[numerical_columns].fillna(0)  #valores numéricos como 0

#calcular 'average_score'
if "critic_score" in df.columns and "people_score" in df.columns:
    df["average_score"] = (df["critic_score"] + df["people_score"]) / 2
else:
    df["average_score"] = 0  #si no existen las columnas, inicializar como 0

#agregar la columna de URLs de pósters
df['poster_url'] = df['title'].apply(get_movie_poster)
df.to_csv("./CSV/peliculas_with_posters.csv", index=False)
print("Posters obtenidos, géneros traducidos, nulos manejados, promedio calculado y dataset guardado.")
