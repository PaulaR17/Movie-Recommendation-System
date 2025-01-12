import pandas as pd

#ruta al archivo de usuarios
USER_DB = "./CSV/users.csv"

#mapeo de traducción de géneros
genre_translation = {
    "Acción": "action",
    "Drama": "drama",
    "Comedia": "comedy",
    "Aventura": "adventure",
    "Terror": "horror",
    "Romance": "romance",
    "Ciencia Ficción": "sci fi"
}

#cargar usuarios
users_df = pd.read_csv(USER_DB)

#traducir géneros
def translate_preferences(preferences):
    if pd.isna(preferences):
        return ""
    translated = [genre_translation.get(genre.strip(), genre) for genre in preferences.split(",")]
    return ','.join(translated)

users_df["preferences"] = users_df["preferences"].apply(translate_preferences)

#guardar los cambios
users_df.to_csv(USER_DB, index=False)
print("Preferencias actualizadas al inglés.")
