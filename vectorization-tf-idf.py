import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # Convert text to numerical values based on word frequency (TF-IDF)

# Read the preprocessed DataFrame
df_preprocess = pd.read_csv("./CSV/preprocessed_peliculas.csv")

# Initialize TfidfVectorizer with a maximum of 10,000 features
tfidf_vectorizer = TfidfVectorizer()

# Select categorical columns (object, category, datetime types)
categorical_columns = df_preprocess.select_dtypes(include=['object', 'category', 'datetime']).columns
df_preprocess_categorical = df_preprocess[categorical_columns].copy()

# Combine all categorical text into a single string per row
df_preprocess_categorical['combined_text'] = df_preprocess_categorical[categorical_columns].astype(str).agg(' '.join, axis=1)

# Fit the TF-IDF vectorizer and transform the combined text
tfidf_matrix = tfidf_vectorizer.fit_transform(df_preprocess_categorical['combined_text'])
"""
.fit --> Learns the vocabulary from the combined_text column and calculates the IDF for the words
.transform --> Converts the text into numerical vectors based on TF-IDF
RESULT --> Sparse matrix where each row represents a movie and each column represents a word
"""

# Create a DataFrame from the TF-IDF matrix with words as column names
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
"""
tfidf_matrix.toarray --> Converts the sparse matrix to a dense array, suitable for DataFrame
columns=tfidf_vectorizer.get_feature_names_out() --> Sets the column names to the extracted words
Each row corresponds to a movie, and each column contains the TF-IDF weight of a word in that movie
"""

# Optional: Print the feature names (words) to verify
print(tfidf_vectorizer.get_feature_names_out())

# Save the TF-IDF DataFrame to CSV without the index and without any extra rows
tfidf_df.to_csv("./CSV/tfidf_matrix_combined.csv", index=False)
