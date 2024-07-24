from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient('mongodb+srv://fernandamorales2001:aBUPss5xf7gkT1k6@proyectobd.ow8lvf0.mongodb.net/admin?authSource=admin&replicaSet=atlas-n58pbl-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true')
db = client['Proyecto']

# Animes con mejores calificaciones en 2020
collection = db['reduced_animelist2']
pipeline = [
    {
        '$group': {
            '_id': '$anime_id',
            'average_rating': {'$avg': '$rating'}
        }
    },
    {
        '$sort': {'average_rating': -1}
    },
    {
        '$limit': 10  # Limitar a los top 10 animes
    }
]

# Ejecutar la consulta y obtener los resultados
result = list(collection.aggregate(pipeline))

# Imprimir los resultados
print("Animes con mejores calificaciones en 2020:")
for doc in result:
    print(f"Anime ID: {doc['_id']}, Calificación Promedio: {doc['average_rating']:.2f}")

# Estudios de animación de animes con más popularidad en 2020
collection_anime = db['anime']
pipeline_studios_popularity = [
    {
        '$group': {
            '_id': '$Studios',
            'total_popularity': {'$sum': '$Popularity'}
        }
    },
    {
        '$sort': {'total_popularity': -1}
    },
    {
        '$limit': 10  # Limitar a los top 10 estudios de animación por popularidad
    }
]

# Ejecutar la consulta y obtener los resultados
result_studios_popularity = list(collection_anime.aggregate(pipeline_studios_popularity))

# Imprimir los resultados
print("\nEstudios de animación de animes con más popularidad en 2020:")
for doc in result_studios_popularity:
    print(f"Estudio: {doc['_id']}, Total de Popularidad: {doc['total_popularity']}")

# Animes con mayor cantidad de episodios
pipeline_most_episodes = [
    {
        '$sort': {'Episodes': -1}  # Ordenar por número de episodios en orden descendente
    },
    {
        '$limit': 10  # Limitar a los top 10 animes con más episodios
    },
    {
        '$project': {
            '_id': 0,
            'Nombre del Anime': '$English name',
            'Número de Episodios': '$Episodes'
        }
    }
]

# Ejecutar la consulta y obtener los resultados
result_most_episodes = list(collection_anime.aggregate(pipeline_most_episodes))

# Imprimir los resultados
print("\nAnimes con mayor cantidad de episodios:")
for doc in result_most_episodes:
    print(f"Nombre: {doc['Nombre del Anime']}, Número de Episodios: {doc['Número de Episodios']}")

client.close()  # Cerrar la conexión a MongoDB
