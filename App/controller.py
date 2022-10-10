"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv
csv.field_size_limit(2147483647)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo plataformas
#Esta función se encargara de que los archivos se puedan ingresar en la carga de datos. 
def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }

    control['model'] = model.newCatalog()
    return control


# Funciones para la carga de datos
#funcion desde loadData - loaddineses la encargada de cargar los datos y encintrar ruta de los archivos

def loadData(control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog=control["model"]
    loadAmazon(catalog)
    loadNetflix(catalog)
    loadHulu(catalog)
    loadDisney(catalog)
    model.loadTotal(catalog)
    
    return catalog


def loadAmazon(catalog):   

    servicefile1 = cf.data_dir + "amazon_prime_titles-utf8-large.csv"
    input_file1 = csv.DictReader(open(servicefile1, encoding='utf-8'))
    for program1 in input_file1:
        del(program1['description'])
        model.addAmazon(catalog,program1)
    return model.amazonSize(catalog) 

def loadNetflix(catalog):

    servicefile2 = cf.data_dir + "netflix_titles-utf8-large.csv"
    input_file2 = csv.DictReader(open(servicefile2, encoding='utf-8'))
    for program2 in input_file2:
        del(program2['description'])
        model.addNetflix(catalog,program2)
    return model.NetflixSize(catalog)

def loadHulu(catalog):

    servicefile3 = cf.data_dir + "hulu_titles-utf8-large.csv"
    input_file3 = csv.DictReader(open(servicefile3, encoding='utf-8'))
    for program3 in input_file3:
        del(program3['description'])
        model.addHulu(catalog,program3)
    return model.HuluSize(catalog)

def loadDisney(catalog):

    servicefile4 = cf.data_dir + "disney_plus_titles-utf8-large.csv"
    input_file4 = csv.DictReader(open(servicefile4, encoding='utf-8'))
    for program4 in input_file4:
        del(program4['description'])
        model.addDisney(catalog,program4)
    return model.DisneySize(catalog)


# Funciones para detemrinar el size de cada una de las plataformas

def sizeAmazon(catalog):
    return model.amazonSize(catalog)

def sizeNetflix(catalog):
    return model.NetflixSize(catalog)

def sizeHulu(catalog):
    return model.HuluSize(catalog)

def sizeDisney(catalog):
    return model.DisneySize(catalog)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

#Requerimiento 1  llama a la funcion de  peliculas estrenadas

def peliculasestrenadas(catalog, anio_int):
    return model.peliculasestrenadas(catalog, anio_int)
    
def seriesestrenadas(catalog, fecha_b):
    return model.seriesestrenadas(catalog,fecha_b)
# Funciones que ayudan a sacar los 3 primeros y ultimos

def primeros3a(catalog):
    """
    Esta función es la que se encarga de buscar los primeros y los ultimos del catalogo ordenado por enunciado 
    luego de eso, se genera una tupla para que pase al view  y se vea en la tabla.
    """
    return (model.primeros_3a(catalog), model.ultimos(catalog))
