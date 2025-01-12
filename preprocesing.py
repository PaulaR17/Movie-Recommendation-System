import pandas as pd
import re  # regular expression operations
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_1():
    def preprocess_text(text):
        text = text.lower()  # Convertimos todo el texto en minúsculas
        text = re.sub(r'[^\w\s\d]', '', text)  #eliminamos caracteres especiales
        tokens = text.split()  #dividimos el texto en palabras individuales
        tokens = [word for word in tokens if word not in stop_words]  #eliminamos stop words
        tokens = [lemmatizer.lemmatize(word) for word in tokens]  #lemmatizamos cada palabra
        return ' '.join(tokens)  #unimos las palabras procesadas en una sola cadena

    df = pd.read_csv("CSV/peliculas.csv")
    print("Dimensiones originales del dataset:", df.shape)
    duplicates = df[df.duplicated(subset=['title'], keep=False)]
    print("Duplicados encontrados:")
    print(duplicates)
    df = df.drop_duplicates(subset=['title'], keep='first')
    print("Dimensiones después de eliminar duplicados:", df.shape)
    df_preprocess = df.copy()
    df_preprocess = df_preprocess.drop('link', axis=1)  #eliminamos la columna 'link'

    df_preprocess = df_preprocess[['id','synopsis', 'consensus', 'type', 'critic_score', 'people_score', 'rating', 'genre',
                                   'original_language', 'director', 'producer', 'writer',
                                   'production_co', 'aspect_ratio', 'crew']]

    categorical_columns = df_preprocess.select_dtypes(include='object').columns
    print(f"Columnas categoricas{categorical_columns}")
    df_preprocess[categorical_columns] = df_preprocess[categorical_columns].fillna("Unknown")  #text as "Unknown"

    numerical_columns = df_preprocess.select_dtypes(include=['float64', 'int64']).columns
    print(f"Columnas numericas {numerical_columns}")
    df_preprocess[numerical_columns] = df_preprocess[numerical_columns].fillna(0)  #numbers as 0
    for col in categorical_columns:
        df_preprocess[col] = df_preprocess[col].apply(preprocess_text)

    print("Preprocesamiento COMPLETADO YAY!")
    return df_preprocess


def tf_idf_2(df_preprocessed):
    # 1) Columnas de texto
    categorical_columns = df_preprocessed.select_dtypes(include='object').columns

    # Combinar texto en 'combined_text'
    df_preprocessed['combined_text'] = df_preprocessed[categorical_columns].astype(str).agg(' '.join, axis=1)

    # Vectorizar con TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_features=10000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_preprocessed['combined_text'])

    # 2) Columnas numéricas
    numerical_columns = df_preprocessed.select_dtypes(include=['float64', 'int64']).columns
    print("Columnas numéricas:", numerical_columns)

    scaler = MinMaxScaler()
    scaled_numerical = scaler.fit_transform(df_preprocessed[numerical_columns])

    # 3) Asignación de pesos
    # Ajusta estos valores según lo que desees
    text_weight = 0.7  # <--- peso para la parte TF-IDF (texto)
    numeric_weight = 0.3  # <--- peso para la parte numérica

    # Convertimos a array para multiplicar
    tfidf_array = tfidf_matrix.toarray()

    # Aplicamos los pesos a cada bloque
    tfidf_array_weighted = tfidf_array * text_weight
    scaled_numerical_weighted = scaled_numerical * numeric_weight

    # 4) Concatenar ambas partes en un solo array de features
    combined_features = np.hstack((tfidf_array_weighted, scaled_numerical_weighted))
    combined_df = pd.DataFrame(combined_features)
    combined_df.to_csv("combined_features_weighted.csv", index=False)
    return combined_df


def calculate_similarity_3(df_preprocessed,combined_df):
    #calcular similitud del coseno
    similarity_matrix = cosine_similarity(combined_df)
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=df_preprocessed['id'],
        columns=df_preprocessed['id']
    )

    similarity_df.to_csv("./CSV/similarity_matrix.csv", index=True)


if __name__ == "__main__":
    df_preprocessed = preprocess_1()
    combined_df = tf_idf_2(df_preprocessed)
    calculate_similarity_3(df_preprocessed,combined_df)

