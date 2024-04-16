import json
import pokebase as pb

def agregar_region(region_id, pokedex_id, region_name):
    # Obtener las versiones de juego que incluyen la región
    region_versions = pb.region(region_id).version_groups
    
    # Obtener la Pokédex de la región
    region_dex = pb.pokedex(pokedex_id)
    
    # Obtener todos los nombres de Pokémon de la región
    region_pokemon_names = [entry.pokemon_species.name for entry in region_dex.pokemon_entries]
    
    # Transformar la información de la región a formato JSON
    region_json_data = {
        "nombre": region_name,
        "juegos_donde_se_incluye": [version.name for version in region_versions],
        "pokemons_que_habitan": region_pokemon_names
    }
    
    # Cargar el archivo JSON existente
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {"regiones": []}  # Crear un nuevo diccionario si el archivo no existe
    
    # Verificar si hay alguna región registrada
    if "regiones" in data:
        # Verificar si la región ya existe
        for existing_region in data["regiones"]:
            if existing_region["nombre"] == region_name:
                print(f"La región {region_name} ya está registrada.")
                return  # Salir de la función si la región ya existe
    
    # Agregar la información de la región al diccionario existente
    data["regiones"].append(region_json_data)
    
    # Guardar el diccionario actualizado de vuelta al archivo JSON
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Agregar la información de las regiones de Kanto y Johto
agregar_region(1, 2, "Kanto")  # ID de Kanto: 1, ID de la Pokédex de Kanto: 2
agregar_region(2, 3, "Johto")  # ID de Johto: 2, ID de la Pokédex de Johto: 3
