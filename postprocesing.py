import pandas as pd
import re #regular expression operations
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

df=pd.read_csv("./CSV/peliculas.csv") #cargamos el archivo csv
print (df.describe(include='all')) #que muestre todo
print (df.info()) #miramos el nombre de las columnas, tipos da datos, valores que faltan...

df_preprocess = df.copy() #se edita esta copia de los datos para hacer to do el preprocesado para el modelo
#dividimos las columnas en no numericas y númericas
numeric_columns=df_preprocess.select_dtypes(include='number').columns  #columnas numericas
non_numeric_columns=df_preprocess.select_dtypes(exclude='number').columns #columnas no numéricas

#estudio de NULLs, miramos que porcentaje de nullos tiene cada columna
null_percentage=df_preprocess.isnull().sum()/len(df_preprocess.index)*100
print ("Porcentaje de NULLs por culumna: ",null_percentage)

#rellenamos todos los NULLs con "unknown"
df_preprocess = df_preprocess.fillna("Unknown")

#descargamos los resucrsos necesarios de nltk (solo pasará una vez)
nltk.download('stopwords')
nltk.download('wordnet')

#empezamos el procesamiento de texto

#columnas no numéricas
stop_words = set(stopwords.words('english')) #cargamos unas stopwords tipics del ingles (the,and,is...) y las convertimos en un conjunto. Lo hacemos para reducir el ruido en el texto
lemmatizer = WordNetLemmatizer() #inicializamos un lematizador, que es la herramienta que reduce las palabras a su forma base.

def preprocess_text(text):
    text=text.lower() #convertimos to do el texto en minúsculas
    text=re.sub(r'[^\w\s\d]','',text) #eliminamos cualquier carácter que no sea una letra (\w) o un espacio (\s) o un número (\d) asi nos quitamos los simbolos de puntuacion o caracteres especiales
    tokens=text.split() #dividimos el texto en palabras individuales
    tokens=[word for word in tokens if word not in stop_words] #eliminamos stop words
    tokens=[lemmatizer.lemmatize(word) for word in tokens] #lematizamos cada palabra
    return ' '.join(tokens) #unimos todas las palabras procesadas en una sola cadena

for col in non_numeric_columns:
    df_preprocess[col] = df_preprocess[col].apply(preprocess_text) #aplicamos el procesamiento de texto a cada celda de las columnas no numéricas

df_preprocess.to_csv("./CSV/preprocessed_peliculas.csv", index=False) #guardamos el dataset procesado

print ("PreProcesamiento COMPLETADO YAY!")