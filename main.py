import pandas as pd

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