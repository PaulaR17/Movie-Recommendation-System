import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Cargar las características combinadas y los títulos
df_features = pd.read_csv("./CSV/combined_features.csv")
df_titles = pd.read_csv("./CSV/peliculas_with_posters.csv")

# Verificar que los IDs sean consistentes
if 'id' not in df_titles.columns:
    raise ValueError("El archivo 'peliculas_with_posters.csv' debe contener una columna 'id'.")

# Generar la matriz de similitud
similarity_matrix = cosine_similarity(df_features)

# Convertir la matriz de similitud en un DataFrame
similarity_df = pd.DataFrame(
    similarity_matrix,
    index=df_titles['id'].astype(str),  # Asegurarse de que los índices sean cadenas
    columns=df_titles['id'].astype(str)
)

# Guardar la matriz de similitud
similarity_df.to_csv("./CSV/cleaned_similarity_matrix_new.csv", index=True)
print("Nueva matriz de similitud generada y guardada en 'cleaned_similarity_matrix.csv'.")
