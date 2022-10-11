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
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate
import datetime as dt



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Buscar las películas estrenadas en un año")
    print("2- Buscar programas de televisión agregados en una fecha determinada")
    #print("3- Contenido donde participa un actor")
    print("4- Contenido de un genero especifico")
    #print("5- Contenido producido en un pais")
    #print("6- Contenido con un director involucrado")
    #print("7- Lista de los top con mas contenido")
    #print("8- seleccionar el tipo de representacion de la lista")

catalog = None
"""
Menu principal
"""

def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def loaddata(control):
    controller.loadData(control)

control = newController()
catalog = control['model']

#El código se encarga de imprimir los tres primeros elementos y los ultimos 3 elementos de cada requerimiento 

def impresionPrimerosUltimos(a):
    primero = lt.getElement(a[0],1)
    segundo = lt.getElement(a[0],2)
    tercero = lt.getElement(a[0],3)
    antepen = lt.getElement(a[1],1)
    penulti = lt.getElement(a[1],2)
    ultimom = lt.getElement(a[1],3)

    print("The first 3 and last 3 titles in content range are")

    table_catalogs_content = [
        [primero['show_id'], primero['type'], primero['title'],primero["director"],primero["cast"],primero["country"],primero["date_added"],primero["release_year"],primero["rating"],primero["duration"],primero["listed_in"],primero["platform"]],
        [segundo['show_id'], segundo['type'], segundo['title'],segundo["director"],segundo["cast"],segundo["country"],segundo["date_added"],segundo["release_year"],segundo["rating"],segundo["duration"],segundo["listed_in"],segundo["platform"]],
        [tercero['show_id'], tercero['type'], tercero['title'],tercero["director"],tercero["cast"],tercero["country"],tercero["date_added"],tercero["release_year"],tercero["rating"],tercero["duration"],tercero["listed_in"],tercero["platform"]],
        [antepen['show_id'], antepen['type'], antepen['title'],antepen["director"],antepen["cast"],antepen["country"],antepen["date_added"],antepen["release_year"],antepen["rating"],antepen["duration"],antepen["listed_in"],antepen["platform"]],
        [penulti['show_id'], penulti['type'], penulti['title'],penulti["director"],penulti["cast"],penulti["country"],penulti["date_added"],penulti["release_year"],penulti["rating"],penulti["duration"],penulti["listed_in"],penulti["platform"]],
        [ultimom['show_id'], ultimom['type'], ultimom['title'],ultimom["director"],ultimom["cast"],ultimom["country"],primero["date_added"],ultimom["release_year"],ultimom["rating"],ultimom["duration"],ultimom["listed_in"],ultimom["platform"]],
        
    ]
    table_size_header = [
        "show_id","type","title","director","cast","country","date_added","release_year","rating","duration","listed_in","platform"
    ]

    print(
        tabulate(table_catalogs_content,headers= table_size_header,tablefmt="grid", maxcolwidths=[None,None,11,None,15,None,None,None,None,None,15,None])
    )



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        loaddata(control)


        
        size_amazon = controller.sizeAmazon(control['model'])
        size_netflix = controller.sizeNetflix(control['model'])
        size_hulu = controller.sizeHulu(control['model'])
        size_disney = controller.sizeDisney(control['model'])

        prim_ulti=controller.primeros3a(control['model']["total"])

        
        
        
        primero = lt.getElement(prim_ulti[0],1)
        

        num=size_amazon+size_disney+size_hulu+size_netflix
        tamaño=len(primero)

        print("-----"*20)

        print("loaded streaming service info:")
        print("Total loeaded titles: " + str(num))
        print("Total loeaded features: " + str(tamaño))

        print("-----"*20)

        table_size_content = [
            ["Amazon", size_amazon],
            ["Netflix", size_netflix],
            ["Hulu", size_hulu],
            ["Disney", size_disney],
        ]
        table_size_header = [
            "Platform", "Amount"
        ]

        print(
            tabulate(table_size_content, headers=table_size_header,tablefmt="grid")
        )
        impresionPrimerosUltimos(prim_ulti)

        
        
    
    elif int(inputs[0]) == 1:
        anio_int = int(input("Año de interés,formato(AAAA): "))
        l = controller.peliculasestrenadas(catalog, anio_int)
        x_size = lt.size(l)
        print("="*10+"Requerimiento No. 1. Inputs"+"="*10)

        print("Movie released in the year: "+str(anio_int))

        print("="*10+"Requerimiento No. 4. Answer"+"="*10)

        
        x1=controller.primeros3a(l)
        print(x1)
    
    elif int(inputs[0]) == 2:
        fechab = input("Ingrese por favor la fecha de interes (yyyy-mm-dd)")
        l = controller.seriesestrenadas(catalog, fechab)
        print(l)
        x_size = lt.size(l)
        print("="*10+"Requerimiento No. 1. Inputs"+"="*10)

        print("Movie released in the year: "+str(fechab))

        print("="*10+"Requerimiento No. 4. Answer"+"="*10)
    
    elif int(inputs[0]) == 4:
        genero = input("Ingrese el genero que desea buscar: ")
        l = controller.buscargenero(catalog,genero)
        print(l)
    
    elif int(inputs[0]) == 7:
        n = int(input("Ingrese el top:"))
        l,size = controller.buscarTOPgenero(catalog,n)
       
       

        
        

    
    else:
        sys.exit(0)

sys.exit(0)


