# CRUD de mascotas
Programa para el sistema Linux/ubuntu que realiza  un CRUD de mascota, donde se puede crear, listar, buscar por id, actualizar y eliminar datos de mascotas usando lenguaje python para su compilación y MongoDB para la base de datos.

## Descripción: 
Al momento de ejecutar el programa, se establece la conexión a la base de datos para que permita manipularla dentro de la terminal. Si se conecta de manera adecuada, se enviará un mensaje de comfirmación y procederá com un menú de opciones para que el usuario decida la interacción que desea realizar. Dependiendo de su elección, se mostrará la función correspondiente.

Dentro de los atributos de Mascota se encuentran el id, el nombre, el tipo y el dueño de la mascota.

## Ejecución:
Para realizar la ejecución del programa, utilize el siguiente comando :
``` bash
python3 noSql.py
``` 

## Dependencias:

 Con el fin de que tenga un buen funcionamiento al momento de ejecutar el script, se requiere las siguientes dependecias:
- python3 o una versión superior.
``` bash 
python3 --version
```
Si se necesita instalar, ocupe el siguiente comando: 
``` bash
sudo apt install python3
```
- python3-pip.
``` bash
sudo apt install python3-pip
```


## Drivers a utilizar:
En relación con permitir la sincronización de la base de datos con python, se rquiere instalar **pymongo** para su funcionamiento.

Para instalarlo se utiliza el comando a continuación :
``` bash
pip install pymongo
```
