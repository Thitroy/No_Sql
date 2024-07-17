import pandas as pd

# Define la ruta al archivo grande
file_path = 'archive/reduced_animelist1.csv'

# Parámetros para la reducción de datos
chunksize = 100000  # Número de filas por chunk
sample_fraction = 0.5  # Proporción de datos a tomar de cada chunk

# Inicializa un DataFrame vacío para almacenar la muestra
sampled_df = pd.DataFrame()

print('Procesando archivo en chunks y tomando una muestra...')

# Procesa el archivo en chunks y toma una muestra de cada chunk
for chunk in pd.read_csv(file_path, chunksize=chunksize):
    # Toma una muestra del chunk
    sampled_chunk = chunk.sample(frac=sample_fraction)
    
    # Concatenar el chunk muestreado al DataFrame final
    sampled_df = pd.concat([sampled_df, sampled_chunk], ignore_index=True)

# Guarda la muestra en un nuevo archivo CSV
sampled_df.to_csv('archive/reduced_animelist2.csv', index=False)

print(f"Archivo reducido guardado como 'archive/reduced_animelist2.csv'")
