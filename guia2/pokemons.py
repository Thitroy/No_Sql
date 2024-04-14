import json
import pokebase as pb

# Obtener las versiones de juego que incluyen la región de Kanto
kanto_versions = pb.region(1).version_groups

# Imprimir las versiones de juego
print("Versiones de juego que incluyen la región de Kanto:")
for version in kanto_versions:
    print("-" + version.name)

 # Agregar una línea en blanco adicional
print()   

# Obtener la Pokédex de la región de Kanto
kanto_dex = pb.pokedex(2)  # El número 2 corresponde a la región de Kanto

# Obtener todos los nombres de Pokémon de la región de Kanto
kanto_pokemon_names = [entry.pokemon_species.name for entry in kanto_dex.pokemon_entries]

# Imprimir el nombre de cada Pokémon de la región de Kanto
print("Nombres de Pokémon dentro de la región de Kanto:")
for name in kanto_pokemon_names:
    print("- " + name)

# Transformar la información a formato JSON
kanto_json_data = {
    "region": "Kanto",
    "versiones_de_juego": [version.name for version in kanto_versions],
    "pokemon_nombres": kanto_pokemon_names
}

# Guardar la información en un archivo JSON
with open('data.json', 'w') as json_file:
    json.dump(kanto_json_data, json_file)

# Mostrar la información en la terminal
print("Información guardada en formato JSON:")
print(json.dumps(kanto_json_data, indent=4))  # Imprimir el JSON con formato indentado
