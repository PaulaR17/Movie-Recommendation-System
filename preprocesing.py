import pandas as pd
import re  # regular expression operations
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preprocess_text(text):
    text = text.lower()  # Convertimos todo el texto en minúsculas
    text = re.sub(r'[^\w\s\d]', '', text)  # Eliminamos caracteres especiales
    tokens = text.split()  # Dividimos el texto en palabras individuales
    tokens = [word for word in tokens if word not in stop_words]  # Eliminamos stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatizamos cada palabra
    return ' '.join(tokens)  # Unimos las palabras procesadas en una sola cadena

#cargar el archivo CSV
df = pd.read_csv("CSV/peliculas.csv")
print("Dimensiones originales del dataset:", df.shape)

#identificar y eliminar duplicados basados en el título
duplicates = df[df.duplicated(subset=['title'], keep=False)]
print("Duplicados encontrados:")
print(duplicates)

#eliminar duplicados conservando la primera aparición
df = df.drop_duplicates(subset=['title'], keep='first')
print("Dimensiones después de eliminar duplicados:", df.shape)

#crear una copia para preprocesamiento
df_preprocess = df.copy()
df_preprocess = df_preprocess.drop('link', axis=1)#eliminamos la columna 'link'

#estudio de NULLs, rellenar con valores predeterminados
null_percentage = df_preprocess.isnull().sum() / len(df_preprocess.index) * 100
print("Porcentaje de NULLs por columna:\n", null_percentage)

categorical_columns = df_preprocess.select_dtypes(include='object').columns
df_preprocess[categorical_columns] = df_preprocess[categorical_columns].fillna("Unknown")#rellenamos texto con "Unknown"

numerical_columns = df_preprocess.select_dtypes(include=['float64', 'int64']).columns
df_preprocess[numerical_columns] = df_preprocess[numerical_columns].fillna(0)#rellenamos números con 0

nltk.download('stopwords')
nltk.download('wordnet')

#inicializamos lematizador y stopwords
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

#procesamos las columnas no numéricas
for col in categorical_columns:
    df_preprocess[col] = df_preprocess[col].apply(preprocess_text)

df_preprocess.to_csv("./CSV/preprocessed_peliculas.csv", index=False)
print("Preprocesamiento COMPLETADO YAY!")
