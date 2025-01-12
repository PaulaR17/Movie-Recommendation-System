from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

#cargar csv
df_features = pd.read_csv("./CSV/combined_features.csv")
df_titles = pd.read_csv("./CSV/preprocessed_peliculas.csv")['title']

#calcular similitud del coseno
similarity_matrix = cosine_similarity(df_features)
similarity_df = pd.DataFrame(similarity_matrix, index=df_titles, columns=df_titles)
similarity_df.to_csv("./CSV/cleaned_similarity_matrix.csv", index=True)

