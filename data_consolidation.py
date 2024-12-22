import pandas as pd

original_df=pd.read_csv("./CSV/peliculas.csv") #el datframe original
tfidf_df=pd.read_csv("./CSV/tfidf_matrix_combined.csv") #el dataframe con el vector TF-IDF

#para asegurarnos miramos los indices y los alineamos, esto es opcional pero lo hacemos para asegurarnos de que las filas de ambos correspondan
assert len(original_df)==len(tfidf_df), "Los datasets tienen tamaños distintos, verefica los datos pls." #mensaje por si sale mal
assert all(original_df.index == tfidf_df.index), "Los índices de las filas no coinciden."
print("Verificación completada: los índices coinciden.")

combined_df=pd.concat([original_df,tfidf_df],axis=1) #combinamos ambos , el axis es para saber como se combinarán, el =1 es para indicar que se combinará por columnas
combined_df.to_csv("./CSV/consolidated_peliculas.csv",index=False) #lo guardamos

print("DataFrames combinados, se ha guardado el nuevo dataframe")