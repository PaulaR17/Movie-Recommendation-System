import pandas as pd

df_preprocess=pd.read_csv("./CSV/preprocessed_peliculas.csv") #el datframe original
tfidf_df=pd.read_csv("./CSV/tfidf_matrix_combined.csv") #el dataframe con el vector TF-IDF

# Utlizar solo las columnas numercias del df_preporcessed
numerical_columns = df_preprocess.select_dtypes(include=['float64', 'int64']).columns

combined_df=pd.concat([df_preprocess[numerical_columns],tfidf_df],axis=1) #combinamos ambos , el axis es para saber como se combinarán, el =1 es para indicar que se combinará por columnas

combined_df.to_csv("./CSV/consolidated_peliculas.csv",index=False) #lo guardamos
print("DataFrames combinados, se ha guardado el nuevo dataframe")