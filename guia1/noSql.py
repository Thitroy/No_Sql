import pprint;

from pymongo.mongo_client import MongoClient
from bson import ObjectId
import sys


uri = "mongodb+srv://user:wA7i8wbcSDd9bfMC@nosql.nydb0ro.mongodb.net/?retryWrites=true&w=majority&appName=noSql"

# Creación de un nuevo cliente y conexión a la base de datos
client = MongoClient(uri)

# Envío de un mensaje para comfirmar la conexión
try:
    client.admin.command('ping')
    print("Se generó la conexión de manera existosa.")
except Exception as e:
    print(e)

db = client['NO-SQL']

collection = db['Mascota']

#  Crear datos 
def createPets():
    nombre = input("Ingrese el nombre de la mascota: ")
    tipo = input("Ingrese el tipo de mascota: ")
    dueño =input("Ingrese el nombre del dueño de la mascota: ")
    id_mascota = ObjectId()


    data = { "_id": id_mascota, "Nombre": nombre, "Tipo": tipo, "Dueño":dueño}
    collection.insert_one(data)
    print(" creación exitosa.")
    pprint.pprint(data)


# Listar todos los datos 
def findPets():
    pets = collection.find({})
    for pet in pets:
        pprint.pprint(pet)

 #Buscar por ID
def findPetsById():
    id = input("Ingrese el id de la mascota que desea buscar: ")
    query = {"_id": ObjectId(id)}
    pet = collection.find_one(query)
    if pet:
        print("Mascota encontrada:")
        pprint.pprint(pet)
    else:
        print("No se encontró la mascota con el id proporcionado.")       

# Actualizar los datos
def updatePets():
    id = input("Ingrese el id de la mascota a actualizar: ")

    query = {"_id": ObjectId(id)}
    pet = collection.find_one(query)
    if not pet:
        print("No se encontró la mascota con el id proporcionado.")
        return

    nombre = input("Ingrese el nombre de la mascota: ")
    nuevo_tipo = input("Ingrese el tipo de mascota: ")
    nuevo_dueño = input("Ingrese el dueño de la mascota: ")
    nueva_data = { "Nombre": nombre, "Tipo": nuevo_tipo, "Dueño":nuevo_dueño}
    collection.update_one(query, {"$set": nueva_data})
    print(" actualización exitosa.")
    pprint.pprint(nueva_data)


 # Eliminar los datos
def deletePets():
    id = input("Ingrese el id de la mascota a eliminar: ")
    query = {"_id": ObjectId(id)}
    pet = collection.find_one(query)

    if  pet:
     collection.delete_one(query)
     print("Eliminación exitosa.")

    else:
     print("No se encontró la mascota con el id proporcionado.")

def exit_p():
    print("Cerrando el programa...")
    sys.exit()


    # Menú de opciones
def menu():
    options = {
        "1": createPets,
        "2": findPets,
        "3": findPetsById,
        "4": updatePets,
        "5": deletePets,
        "6": exit_p
    }

    while True:
        print("\nSelecciona una opción:")
        print("1. Crear datos de mascota")
        print("2. Buscar mascotas")
        print("3. Buscar una mascota")
        print("4. Actualizar datos de mascota")
        print("5  Eliminar datos de mascota")
        print("6. Salir")


        opcion = input("Ingrese el número de la opción: ")

        selected_option = options.get(opcion)
        if selected_option:
            selected_option()
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")


if __name__ == "__main__":
 menu()
