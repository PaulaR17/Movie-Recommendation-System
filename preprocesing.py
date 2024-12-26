import pandas as pd
import re  # regular expression operations
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Function for text preprocessing
def preprocess_text(text):
    text = text.lower()  # Convertimos todo el texto en minúsculas
    text = re.sub(r'[^\w\s\d]', '', text)  # Eliminamos caracteres especiales
    tokens = text.split()  # Dividimos el texto en palabras individuales
    tokens = [word for word in tokens if word not in stop_words]  # Eliminamos stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatizamos cada palabra
    return ' '.join(tokens)  # Unimos las palabras procesadas en una sola cadena

# Load the original CSV file
df = pd.read_csv("CSV/peliculas.csv")
print("Dimensiones originales del dataset:", df.shape)

# Identify and remove duplicates based on the title
duplicates = df[df.duplicated(subset=['title'], keep=False)]
print("Duplicados encontrados:")
print(duplicates)

df = df.drop_duplicates(subset=['title'], keep='first')
print("Dimensiones después de eliminar duplicados:", df.shape)

# Create a copy for preprocessing
df_preprocess = df.copy()
df_preprocess = df_preprocess.drop('link', axis=1)  # Eliminamos la columna 'link'

# Initialize lemmatizer and stopwords
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Fill NULL values
categorical_columns = df_preprocess.select_dtypes(include='object').columns
df_preprocess[categorical_columns] = df_preprocess[categorical_columns].fillna("Unknown")  # Text as "Unknown"

numerical_columns = df_preprocess.select_dtypes(include=['float64', 'int64']).columns
df_preprocess[numerical_columns] = df_preprocess[numerical_columns].fillna(0)  # Numbers as 0

# Process non-numerical columns
for col in categorical_columns:
    df_preprocess[col] = df_preprocess[col].apply(preprocess_text)

# Save the preprocessed data to CSV
df_preprocess.to_csv("./CSV/preprocessed_peliculas.csv", index=False)
print("Preprocesamiento COMPLETADO YAY!")
