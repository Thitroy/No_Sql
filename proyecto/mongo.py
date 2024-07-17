from pymongo import MongoClient
import json
import glob
import os

# Ruta a la carpeta que contiene los archivos JSON
json_folder_path = 'archive/'

# Obtener todos los archivos JSON en la carpeta
json_files = glob.glob(os.path.join(json_folder_path, '*.json'))

# Conectar a MongoDB
client = MongoClient('mongodb+srv://fernandamorales2001:aBUPss5xf7gkT1k6@proyectobd.ow8lvf0.mongodb.net/admin?authSource=admin&replicaSet=atlas-n58pbl-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true')
db = client['Proyecto']

# Procesar cada archivo JSON
for json_file in json_files:
    if os.path.exists(json_file):
        print(f"Cargando archivo JSON: {json_file}")
        
        # Leer el archivo JSON
        with open(json_file) as file:
            json_data = json.load(file)
        
        # Nombre de la colección basado en el nombre del archivo
        collection_name = os.path.basename(json_file).replace('.json', '')
        collection = db[collection_name]
        
        # Insertar datos en la colección
        collection.insert_many(json_data)
        
        print(f"Datos cargados en la colección: {collection_name}")
    else:
        print(f"Archivo JSON no encontrado: {json_file}")
