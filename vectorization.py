import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer #convertir texto en valores numéricos basandonos en la frecuencia de palabras (TF-IDF)
from preprocesing import df_preprocess

df_preprocess = pd.read_csv("./CSV/preprocessed_peliculas.csv") #leemos el datafreme preprocesado que hemos creado en el script postprocesing

tfidf_vectorizer = TfidfVectorizer(max_features=10000) #creamos una instancia de tfidvectorizer y le ponemos que solo coja las 10.000 palabras más importantes para optimizar
tfidf_matrix = tfidf_vectorizer.fit_transform(df_preprocess['combined_text'])
"""
.fit --> aprende el vocabulario del texto en la columna combined_text y calcula el IDF para las palabras
transform --> convierte el texto en vectores numéricos basados en TF-IDF
RESULTADO --> matriz dispersa, cada fila representa una película y cada columna una palabra
"""
tfidf_df=pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
"""
tfidf_matrix.toarray --> convierte la matriz en una matriz densa, que se puede convertir en un dataframe
columns=tfidf_vectorizer.get_feature_names_out --> obtiene las caracteristicas de las palabras que represetnan las columnas del dataframe
cada fila correspone a una peli y cada columna tiene el peso TF-IDF de una palabra en esa pelicula
"""
print(tfidf_vectorizer.get_feature_names_out())
tfidf_df.to_csv("./CSV/tfidf_matrix_combined.csv", index=False)

