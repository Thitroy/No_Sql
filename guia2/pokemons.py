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