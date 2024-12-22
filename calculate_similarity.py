import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity #para calcular la similitud del coseno
import numpy as np #para trabajar con operaciones numericas

df=pd.read_csv("./CSV/tfidf_matrix_with_original.csv") #el dataframe con to do consolidado
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

df_numerical = df[numerical_columns].copy()
similarity_matrix = cosine_similarity(df_numerical) #calculamos la similitud del coseno y lo pone en una matriz cuadrada de tamaño nxn, n número de peliculas, con valores entre 0 (no se parecen en nada) y 1 (idénticos)
#ahora queremos convertir esta matriz de similitud en un dataframe para insepccion
similarity_df = pd.DataFrame(similarity_matrix, index=df['title'], columns=df['title'])
#asignamos los nombres de las pelis como indices y columnas, para faciliar asi el ver que tan similares son las pelis entre si
similarity_df.to_csv("./CSV/similarity_matrix.csv")
print("Similitudes guardadas.")
