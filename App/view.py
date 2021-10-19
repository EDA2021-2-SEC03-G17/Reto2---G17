"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import sys
import controller
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#MENU

def printMenu():
    print("___________________________________________")
    print("    BIENVENIDO AL CATALOGO DE MoMA'S")
    print("___________________________________________")
    print("")
    print("1 ) Cargar información en el catálogo")
    print("2 ) Obras mas antiguas por medio")
    print("3 ) Numero total de obras por nacionalidad")
    print("4 ) Prueba req 2")
    print("5 ) Prueba req 4")
    print("0 ) Salir")
    print("")
    print("___________________________________________")

#CARGA DE DATOS [1]
def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

catalog = None

#REQ1 [2]

def medioAntiguo(catalog):
    num=int(input("Ingrese el numero de obras que quiere ver: "))
    medio=input("Ingrese el medio que desea consultar: ")
    antiguos=controller.medioAntiguo(catalog,num,medio)
    return antiguos

#REQ2 [3]
def numeroObrasNacionalidad(catalog):
    nation = input("Ingrese la nacionalidad que quiere consultar\n")
    resultado = controller.obrasNacionalidad(catalog, nation)
    return resultado

def obrasporNacionalidad(catalog):
    mapa = controller.obrasporNacionalidad(catalog)
    return mapa

#MENU PRINCIPAL

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....") 
        catalog = initCatalog()
        loadData(catalog)
        print(" ")
        print('Artistas cargadas: ' + str(controller.ArtistsSize(catalog)))
        print(" ")
        print('Obras cargadas: ' + str(controller.ArtworksSize(catalog)))
        print(" ")

    elif int(inputs[0]) == 2:
        lista=medioAntiguo(catalog)
        print(lista)
    
    elif int(inputs[0]) == 3:
        lista = numeroObrasNacionalidad(catalog)
        print(lista)

    elif int(inputs[0]) == 4:
        date1 = input('Ingrese la fecha 1 con el formato YYYY-MM-DD\n')
        date2 = input('Ingrese la fecha 2 con el formato YYYY-MM-DD\n')
        resultado = controller.artworksbyDate(date1, date2, catalog)
        print(resultado)
    
    elif int(inputs[0]) == 5:
        lista = controller.obrasporNacionalidad(catalog)
        print(lista)
    else:
        sys.exit(0)
sys.exit(0)
