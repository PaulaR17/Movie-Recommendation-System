import pandas as pd

#cargar el archivo
file_path = "CSV/cleaned_similarity_matrix.csv"
similarity_matrix = pd.read_csv(file_path)

#limpiar los datos: eliminar puntos como separadores de miles y convertir a números
for column in similarity_matrix.columns[2:]:
    similarity_matrix[column] = (
        similarity_matrix[column]
        .astype(str)  #convertir a string para aplicar operaciones de texto
        .str.replace(".", "", regex=False)  #eliminar los puntos
        .replace("None", None)  #manejar valores no válidos
        .astype(float)  #convertir a números
    )

#revisar los primeros valores procesados
print(similarity_matrix.head())
