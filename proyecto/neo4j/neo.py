import os
from neo4j import GraphDatabase
import json
from neo4j.exceptions import ServiceUnavailable


# Configuración de la conexión
uri = "bolt://localhost:7687"
username = "neo4j"  # Reemplaza con tu nombre de usuario de Neo4j
password = "Splinth785"  # Reemplaza con tu contraseña de Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

# Función para cargar datos desde JSON a Neo4j sin usar APOC
def load_data_to_neo4j(session, json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        for record in data:
            session.run("""
            MERGE (a:Anime {anime_id: $anime_id})
            SET a.name = $name,
                a.genre = $genre,
                a.episodes = $episodes,
                a.popularity = $popularity,
                a.studios = $studios
            """, 
            anime_id=record.get('MAL_ID'),
            name=record.get('English name'),
            genre=record.get('Genres'),
            episodes=record.get('Episodes'),
            popularity=record.get('Popularity'),
            studios=record.get('Studios'))

# Verifica la conexión a Neo4j
def verify_connection():
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            result = session.run("RETURN 1")
            if result.single()[0] == 1:
                print("Conexión a Neo4j verificada exitosamente.")
        return driver
    except ServiceUnavailable as e:
        print(f"No se puede establecer una conexión con Neo4j: {e}")
        return None

# Ruta a la carpeta que contiene los archivos JSON
json_folder_path = 'D:/cursos/BD_Semestral/proyecto/archive/'

# Obtener todos los archivos JSON en la carpeta
json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]

# Función para ejecutar las consultas
def execute_queries(session):
    # Estudios de animación de animes con más popularidad en 2020
    print("\nEstudios de animación de animes con más popularidad en 2020:")
    query1 = """
    MATCH (a:Anime)
    WHERE a.popularity IS NOT NULL
    WITH a.studios AS studio, SUM(a.popularity) AS total_popularity
    RETURN studio, total_popularity
    ORDER BY total_popularity DESC
    LIMIT 10
    """
    result1 = session.run(query1)
    for record in result1:
        print(f"Estudio: {record['studio']}, Popularidad Total: {record['total_popularity']}")

    # Animes con mayor cantidad de episodios
    print("\nAnimes con mayor cantidad de episodios:")
    query2 = """
    MATCH (a:Anime)
    WHERE a.episodes IS NOT NULL
    RETURN a.name AS anime, a.episodes AS episodes
    ORDER BY episodes DESC
    LIMIT 10
    """
    result2 = session.run(query2)
    for record in result2:
        print(f"Anime: {record['anime']}, Número de Episodios: {record['episodes']}")

    # Animes más populares
    print("\nAnimes más populares:")
    query3 = """
    MATCH (a:Anime)
    WHERE a.popularity IS NOT NULL
    RETURN a.name AS anime, a.popularity AS popularity
    ORDER BY popularity DESC
    LIMIT 10
    """
    result3 = session.run(query3)
    for record in result3:
        print(f"Anime: {record['anime']}, Popularidad: {record['popularity']}")


# Verifica la conexión y procesa los archivos
driver = verify_connection()
if driver:
    with driver.session() as session:
        print("Cargando datos en Neo4j...")
        load_data_to_neo4j(session, os.path.join(json_folder_path, 'anime.json'))
        print("Datos cargados exitosamente en Neo4j")
        execute_queries(session)
    driver.close()
else:
    print("No se pudo conectar a Neo4j. Por favor, verifica que el servidor esté corriendo y que las credenciales sean correctas.")