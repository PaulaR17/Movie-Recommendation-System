from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

df_preprocessed = pd.read_csv("./CSV/preprocessed_peliculas.csv")
print("Shape of df_preprocessed:", df_preprocessed.shape)

#columnas categoricas
categorical_columns = df_preprocessed.select_dtypes(include='object').columns
df_preprocessed['combined_text'] = df_preprocessed[categorical_columns].astype(str).agg(' '.join, axis=1)

# Vectorize con TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=10000)
tfidf_matrix = tfidf_vectorizer.fit_transform(df_preprocessed['combined_text'])

#normalizar columnas numericas
numerical_columns = df_preprocessed.select_dtypes(include=['float64', 'int64']).columns
scaler = MinMaxScaler()
scaled_numerical = scaler.fit_transform(df_preprocessed[numerical_columns])

#combinarlo con la matriz TF-IDF
combined_features = np.hstack((tfidf_matrix.toarray(), scaled_numerical))
combined_df = pd.DataFrame(combined_features)
combined_df.to_csv("./CSV/combined_features.csv", index=False)
