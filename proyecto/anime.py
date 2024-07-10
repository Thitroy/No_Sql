import pandas as pd
import glob
import os
from sklearn.preprocessing import StandardScaler
from pymongo import MongoClient

# Define la ruta a la carpeta donde están los archivos CSV
path = 'archive'

# Usa glob para encontrar todos los archivos CSV en esa ruta
all_files = glob.glob(os.path.join(path, "*.csv"))

# Lista para almacenar los DataFrames de cada archivo
dfs = []

# Procesar cada archivo CSV y agregarlo a la lista dfs
for file in all_files:
    print(f"Leyendo archivo: {file}")
    try:
        # Muestreo aleatorio para reducir el tamaño de animelist.csv si es necesario
        if file.endswith('animelist.csv'):
            df = pd.read_csv(file, nrows=1)  # Leer solo las primeras 90 filas
            dfs.append(df)
        else:
            df = pd.read_csv(file)
            dfs.append(df)
    except Exception as e:
        print(f"Error al procesar el archivo {file}: {str(e)}")

# Combinar todos los DataFrames en uno solo
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    print("Archivos combinados en un solo DataFrame.")

    # Proceso ETL - Limpieza y transformación de datos
    try:
        # Convertir tipos de datos si es necesario
        combined_df['user_id'] = pd.to_numeric(combined_df['user_id'], errors='coerce')
        combined_df['anime_id'] = pd.to_numeric(combined_df['anime_id'], errors='coerce')
        combined_df['date'] = pd.to_datetime(combined_df['date'], errors='coerce')

        # Eliminar filas con valores nulos
        combined_df = combined_df.dropna(subset=['user_id', 'anime_id', 'date', 'rating'])

        # Normalizar/Estandarizar la columna 'rating'
        scaler = StandardScaler()
        combined_df['rating'] = scaler.fit_transform(combined_df[['rating']])

        # Filtrar animes con un rating mayor a 8
        combined_df = combined_df[combined_df['rating'] > 8]

        # Crear una nueva columna 'rating_normalizado'
        combined_df['rating_normalizado'] = (combined_df['rating'] - combined_df['rating'].min()) / (combined_df['rating'].max() - combined_df['rating'].min())

        # Mostrar información del DataFrame combinado
        print("DataFrame combinado y procesado:")
        print(combined_df.head())
        print(combined_df.info())

        # Conectar a MongoDB y guardar los datos
        client = MongoClient('mongodb+srv://fernandamorales2001:aBUPss5xf7gkT1k6@proyectobd.ow8lvf0.mongodb.net/admin?authSource=admin&replicaSet=atlas-n58pbl-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true')
        db = client['Proyecto']  # Nombre de la base de datos
        collection = db['Anime']  # Nombre de la colección

        # Convertir el DataFrame combinado a un diccionario de diccionarios para insertarlo en MongoDB
        data_dict = combined_df.to_dict("records")

        # Insertar los datos en la colección de MongoDB
        collection.insert_many(data_dict)

        print("Datos insertados en MongoDB")
    except Exception as e:
        print(f"Error en el proceso ETL: {str(e)}")
else:
    print("No se encontraron archivos CSV válidos para procesar.")



try:
    # Consulta 1: Animes más recomendados de 2020
    print("Animes más recomendados de 2020:")
    cursor = collection.find().sort("recommendations", -1).limit(10)
    for anime in cursor:
        print(anime['title'], anime['recommendations'])

    print("\n")

    # Consulta 2: Géneros más populares en 2020
    print("Géneros más populares en 2020:")
    pipeline_genres = [
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    cursor_genres = collection.aggregate(pipeline_genres)
    for genre in cursor_genres:
        print(genre['_id'], genre['count'])

    print("\n")

    # Consulta 3: Relaciones entre géneros y calificaciones promedio en 2020
    print("Relaciones entre géneros y calificaciones promedio en 2020:")
    pipeline_avg_rating = [
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "avgRating": {"$avg": "$rating"}}},
        {"$sort": {"avgRating": -1}}
    ]
    cursor_avg_rating = collection.aggregate(pipeline_avg_rating)
    for genre in cursor_avg_rating:
        print(genre['_id'], genre['avgRating'])

except Exception as e:
    print(f"Error en la consulta: {str(e)}")

finally:
    # Cerrar la conexión a MongoDB
    client.close()