import pandas as pd

# Cargar el archivo
file_path = "CSV/cleaned_similarity_matrix.csv"
similarity_matrix = pd.read_csv(file_path)

# Limpiar los datos: eliminar puntos como separadores de miles y convertir a números
for column in similarity_matrix.columns[2:]:
    similarity_matrix[column] = (
        similarity_matrix[column]
        .astype(str)  # Convertir a string para aplicar operaciones de texto
        .str.replace(".", "", regex=False)  # Eliminar los puntos
        .replace("None", None)  # Manejar valores no válidos
        .astype(float)  # Convertir a números
    )

# Revisar los primeros valores procesados
print(similarity_matrix.head())
