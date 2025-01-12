import pandas as pd

original_csv_path = "CSV/peliculas.csv"
original_df = pd.read_csv(original_csv_path)
similarity_matrix_path = "CSV/cleaned_similarity_matrix.csv"
updated_similarity_df = pd.read_csv(similarity_matrix_path)

#mapear titulos originales
corrected_titles = original_df['title'].drop_duplicates().reset_index(drop=True)
updated_similarity_df['title'] = corrected_titles
corrected_similarity_matrix_path = "CSV/corrected_similarity_matrix.csv"
updated_similarity_df.to_csv(corrected_similarity_matrix_path, index=False)
