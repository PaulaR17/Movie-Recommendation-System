import pandas as pd

df=pd.read_csv("./CSV/peliculas.csv") #cargamos el archivo csv

print (df.head()) #miramos las primeras filas
print (df.describe(include='all')) #que muestre todo
print (df.info()) #miramos el nombre de las columnas, tipos da datos, valores que faltan...

