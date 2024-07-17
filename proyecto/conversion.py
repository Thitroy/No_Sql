import pandas as pd
import json
import glob
import os

def clean_data(df):
    # Eliminar filas con valores nulos
    df.dropna(inplace=True)
    
    # Eliminar duplicados
    df.drop_duplicates(inplace=True)
    
    # Convertir los datos a los tipos apropiados
    if 'user_id' in df.columns:
        df['user_id'] = df['user_id'].astype(int)
    if 'anime_id' in df.columns:
        df['anime_id'] = df['anime_id'].astype(int)
    if 'rating' in df.columns:
        df['rating'] = df['rating'].astype(float)
    
    # Filtrar filas con valores de 'rating' fuera del rango 0-10
    if 'rating' in df.columns:
        df = df[(df['rating'] >= 0) & (df['rating'] <= 10)]
    
    return df

# Ruta a la carpeta que contiene los archivos CSV
csv_folder_path = 'archive/'

# Obtener todos los archivos CSV en la carpeta
csv_files = glob.glob(os.path.join(csv_folder_path, '*.csv'))

# Procesar cada archivo CSV
for csv_file in csv_files:
    if os.path.exists(csv_file):
        print(f"Procesando archivo: {csv_file}")
        
        # Cargar el archivo CSV en trozos
        chunk_iter = pd.read_csv(csv_file, chunksize=5000)
        clean_chunks = []
        
        for chunk in chunk_iter:
            # Limpiar los datos
            clean_chunk = clean_data(chunk)
            clean_chunks.append(clean_chunk)
        
        # Concatenar todos los trozos limpios
        clean_df = pd.concat(clean_chunks)
        
        # Convertir el DataFrame limpio a una lista de diccionarios (formato JSON)
        json_data = clean_df.to_dict('records')
        
        # Nombre del archivo JSON de salida
        json_file_name = os.path.basename(csv_file).replace('.csv', '.json')
        json_file_path = os.path.join(csv_folder_path, json_file_name)
        
        # Guardar el JSON en un archivo
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)
        
        print(f"Archivo JSON creado: {json_file_path}")
    else:
        print(f"Archivo no encontrado: {csv_file}")
