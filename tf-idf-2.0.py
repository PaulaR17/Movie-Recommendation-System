import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Read the preprocessed DataFrame
df_preprocess = pd.read_csv("./CSV/preprocessed_peliculas.csv")
print("Shape of df_preprocess:", df_preprocess.shape)

# 2. Initialize TfidfVectorizer (up to 10,000 features)
tfidf_vectorizer = TfidfVectorizer(max_features=10000)

# 3. Select categorical columns (object, category, datetime)
categorical_columns = df_preprocess.select_dtypes(
    include=['object', 'category', 'datetime']
).columns

# 4. Combine all categorical text into a single string per row
df_preprocess_categorical = df_preprocess[categorical_columns].copy()
print("Shape of df_preprocess_categorical:", df_preprocess_categorical.shape)

df_preprocess_categorical['combined_text'] = df_preprocess_categorical.astype(str).agg(' '.join, axis=1)
print("Shape of df_preprocess_categorical:", df_preprocess_categorical.shape)

# 5. Fit the TF-IDF vectorizer and transform the combined text
tfidf_matrix = tfidf_vectorizer.fit_transform(df_preprocess_categorical['combined_text'])
print("TF-IDF matrix shape:", tfidf_matrix.shape)

# 6. Convert TF-IDF matrix to DataFrame (dense)
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=tfidf_vectorizer.get_feature_names_out()
)

print("Shape of tfidf_df:", tfidf_df.shape)

# 7. (Optional) If you want to combine TF-IDF columns with all your original columns:
df_combined = pd.concat([df_preprocess.reset_index(drop=True), tfidf_df], axis=1)
print("Combined DataFrame shape:", df_combined.shape)
# Expect (1600, original_num_cols + d)

# 8. Save TF-IDF features alone OR the combined DataFrame to CSV
df_combined.to_csv("./CSV/tfidf_matrix_with_original.csv", index=False)
