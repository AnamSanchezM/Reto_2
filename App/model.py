﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mg
import datetime as dt
assert cf
import time
from time import strptime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos 

#Creamos un catalogo donde son listas de diccionarios y en el total se encuentra el catalogo con todas las plataformas. 
#Desde la linea 43-62 es el código para la carga de datos, mas abajo se pondrá la funcion que los ordene por lo solicitado. (Enunciado)

def newCatalog():
    """
    Se inicializa el catalog con diccionarios con la llave de las plataformas
    retorna un catalogo completo. 
    """
    catalog = {}
    catalog["Amazon"] = lt.newList("ARRAY_LIST",cmpByReleaseYear)
    catalog["Netflix"] = lt.newList("ARRAY_LIST",cmpByReleaseYear)
    catalog["Hulu"] = lt.newList("ARRAY_LIST",cmpByReleaseYear)
    catalog["Disney"] = lt.newList("ARRAY_LIST",cmpByReleaseYear)
    catalog['total'] = lt.newList("ARRAY_LIST",cmpByReleaseYear)
    catalog["años"] = mp.newMap(200,maptype="PROBING",loadfactor=0.5)
    catalog["datel"] = mp.newMap(8000, maptype = "PROBING", loadfactor=0.5)
    catalog["genre"] = mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    

    

    return catalog

# Funciones para agregar informacion al catalogo

def loadTotal(catalog):
    """
        Es la encargada de decirnos en cual de las plataformas se encuentra cada uno de los diccionarios
        de la lista si es amazon, netflix, hulu y disnay 
    Args:
        catalog (_type_): _description_
    """
    size_amazon = lt.size(catalog["Amazon"])
    for i in range(0, size_amazon):
        a = lt.getElement(catalog["Amazon"], i)
        a["platform"] = "Amazon"
        lt.addLast(catalog["total"], a)
        addmovieperyear(catalog,a)
        addtvshowperdate(catalog,a)
        busqueda_genero(catalog,a)

    size_netflix = lt.size(catalog["Netflix"])
    for n in range(0, size_netflix):
        n = lt.getElement(catalog["Netflix"], n)
        n["platform"] = "Netflix"
        lt.addLast(catalog["total"], n)
        addmovieperyear(catalog,n)
        addtvshowperdate(catalog,n)
        busqueda_genero(catalog,n)


    size_hulu=lt.size(catalog["Hulu"])
    for h in range(0, size_hulu):
        h=lt.getElement(catalog["Hulu"],h)
        h["platform"] = "Hulu"
        lt.addLast(catalog["total"], h)
        addmovieperyear(catalog,h)
        addtvshowperdate(catalog,h)
        busqueda_genero(catalog,h)

    
    size_disney = lt.size(catalog["Disney"])
    for d in range(0,size_disney):
        d = lt.getElement(catalog["Disney"],d)
        d["platform"]="Disney"
        lt.addLast(catalog["total"], d)
        addmovieperyear(catalog,d)
        addtvshowperdate(catalog,d)
        busqueda_genero(catalog,d)
    

    
    lista=mergesortyear(catalog["total"])

def addAmazon(catalog, programa1):
    listaAmazon = catalog['Amazon']

    if programa1['duration'] != '':
        duracion = programa1['duration'].split(' ')
        programa1['duration'] = int(duracion[0])
    else:
        programa1['duration'] = 0
    lt.addLast(listaAmazon, programa1)

def addNetflix(catalog, programa2):
    listaNetflix = catalog['Netflix']
    

    if programa2['duration'] != '':
        duracion = programa2['duration'].split(' ')
        programa2['duration'] = int(duracion[0])
    else:
        programa2['duration'] = 0
    lt.addLast(listaNetflix, programa2)

def addHulu(catalog, programa3):

    if programa3['duration'] != '':
        duracion = programa3['duration'].split(' ')
        programa3['duration'] = int(duracion[0])
    else:
        programa3['duration'] = 0
    lt.addLast(catalog["Hulu"], programa3)

def addDisney(catalog, programa4):

    if programa4['duration'] != '':
        duracion = programa4['duration'].split(' ')
        programa4['duration'] = int(duracion[0])
    else:
        programa4['duration'] = 0

    lt.addLast(catalog["Disney"], programa4)


#================ Requerimiento 1 en el reto 2 ayuda a la carga de datos ==============================
   
def addmovieperyear(catalog,movie):
    mapa = catalog["años"]
    if movie["type"]=="Movie":
        if (movie['release_year'] != ''):
            rel_year = movie['release_year']
            rel_year = int(float(rel_year))
        else:
            rel_year = 2020
        existyear = mp.contains(mapa, rel_year)
        if existyear:
            entry = mp.get(mapa, rel_year)
            year = me.getValue(entry)
        else:
            year = newYear(rel_year)
            mp.put(mapa, rel_year, year)
        lt.addLast(year['peliculas'], movie)

def newYear(rel_year):
    """
    Esta funcion crea la estructura de peliculas asociados
    a un año.
    """
    entry = {'year': "", "peliculas": None}
    entry['year'] = rel_year
    entry['peliculas'] = lt.newList('ARRAY_LIST', cmpBytitle)
    return entry


#================ Requerimiento 2 en el reto 2 ayuda a la carga de datos ==============================
   
def addtvshowperdate(catalog,serie):
    """
    En la primera linea se pasa el mapa creado en el catalogo, se realiza un if para 
    mirar si es una serie, luego lo que se hace es que se saca la info de la date_added
    se pone en el formato para que retorne la fecha esperada luego se empiezan a agregar
    en los diccionarios. 
    Se espera que esta función haga un mapa con las fechas de las series y sea agregado
    en el catalogo. 

    Args:
        catalog (_type_): catalogo creado donde esta la info
        serie (_type_): es el contenido que se le pasa a la función para que en los ciclos
        se genere la información
    """
    mapa = catalog["datel"]
    if serie["type"]=="TV Show":
        
        fecha=serie["date_added"].strip()
        fecha_f= ""
        if fecha != "":
            fecha=strptime(fecha,"%B %d, %Y")
            fecha_f = str(fecha[0])+"-"+str(fecha[1])+"-"+str(fecha[2])
        
            if (fecha_f!= ''):
                add_date = fecha_f
            else:
                add_date = 2020
            existyear = mp.contains(mapa, add_date)
            if existyear:
                entry = mp.get(mapa, add_date)
                date = me.getValue(entry)
            else:
                date = newDate(add_date)
                mp.put(mapa, add_date, date)
            lt.addLast(date['series'], serie)

def newDate(add_date):
    """
    Esta funcion crea la estructura de peliculas asociados
    a un año.
    """
    entry = {'date': "", "series": None}
    entry['date'] = add_date
    entry['series'] = lt.newList('ARRAY_LIST', cmpBytitle)
    return entry

#======================= Requerimiento 4 en el reto 2 ayuda a la carga de datos ==============================
def busqueda_genero(catalog,content):
    """

    Args:
        catalog (_type_): _description_
        content (_type_): _description_
    """
    mapa_genero=catalog["genre"]
    if (content['listed_in'] != ''):
        list_genero = content["listed_in"].split(",")
     
        for i in list_genero:  
            i= i.strip()  
            existgenre = mp.contains(mapa_genero, i)
            if existgenre:
                entry = mp.get(mapa_genero, i)
                valor = me.getValue(entry)
            else:
                valor = newgenero(i)
                mp.put(mapa_genero, i, valor)
            lt.addLast(valor['contenido'], content)
            mapa_contadores=valor["contadores"]
            contador_general=me.getValue(mp.get(mapa_contadores,"contenido_total"))+1
            mp.put(mapa_contadores,"contenido_total",contador_general)
            if content["type"] == "Movie":
                contador=me.getValue(mp.get(mapa_contadores,"Peli"))+1
                mp.put(mapa_contadores,"Peli",contador)

            elif content["type"] == "TV Show":
                contador=me.getValue(mp.get(mapa_contadores,"Serie"))+1
                mp.put(mapa_contadores,"Serie",contador)
            
            if content["platform"]=="Amazon":
                contador=me.getValue(mp.get(mapa_contadores,"Amazon"))+1
                mp.put(mapa_contadores,"Amazon",contador)
            
            if content["platform"]=="Netflix":
                contador=me.getValue(mp.get(mapa_contadores,"Netflix"))+1
                mp.put(mapa_contadores,"Netflix",contador) 
            
            if content["platform"]=="Hulu":
                contador=me.getValue(mp.get(mapa_contadores,"Hulu"))+1
                mp.put(mapa_contadores,"Hulu",contador) 

            if content["platform"]=="Disney":
                contador=me.getValue(mp.get(mapa_contadores,"Disney"))+1
                mp.put(mapa_contadores,"Disney",contador) 


def newgenero(genre):
    """
    Esta funcion crea la estructura de peliculas asociados
    a un año.
    """
    entry = {'genero': "", "contenido": None, "contadores" : None}
    entry["contadores"] = mp.newMap(10,maptype="PROBING",loadfactor=0.5)
    entry['genero'] = genre
    entry['contenido'] = lt.newList('ARRAY_LIST', cmpBytitle)
    mp.put(entry["contadores"],"contenido_total",0)
    mp.put(entry["contadores"],"Peli",0)
    mp.put(entry["contadores"],"Serie",0)
    mp.put(entry["contadores"],"Amazon",0)
    mp.put(entry["contadores"],"Netflix",0)
    mp.put(entry["contadores"],"Hulu",0)
    mp.put(entry["contadores"],"Disney",0)


    
    return entry


# Funciones para creacion de datos

#Desde la función amazonSize, hasta Disneysize, calculamos los size de los catalogos de cada plataforma
def amazonSize(catalog):
    return (lt.size(catalog['Amazon']))

def NetflixSize(catalog):
    return (lt.size(catalog['Netflix']))

def HuluSize(catalog):
    return (lt.size(catalog['Hulu']))

def DisneySize(catalog):
    return (lt.size(catalog['Disney']))


# Funciones de consulta

#COMIENZO DE LOS REQUERIMIENTOS ================================

#REQUERIMIENTO 1 

def peliculasestrenadas(catalog, anio_int):
    
    l = mp.get(catalog["años"],anio_int)
    l = me.getValue(l)
    l = l["peliculas"]

    listed_list = mg.sort(l, cmpBytitle)
    
    return listed_list

#REQUERIMIENTO 2 ======== NO ESTÁ COMPILANDO LA INFORMACIÓN

def seriesestrenadas(catalog, fecha_b):
    
    l = mp.get(catalog["datel"],fecha_b)
    
    l = me.getValue(l)
    l = l["series"]

    listed_list = mg.sort(l, cmpBytitle)
    
    return listed_list


#REQUERIMIENTO 4 

def buscar_genero(catalog, genero):
    """_summary_

    Args:
        catalog (_type_): _description_
        genero (_type_): _description_

    Returns:
        _type_: _description_
    """
    l = mp.get(catalog["genre"],genero)
    l = me.getValue(l)
    lista = l["contenido"]
    
    listed_list = mg.sort(lista, cmpreq4)
        
    return listed_list, me.getValue(mp.get(l["contadores"],"Peli")),me.getValue(mp.get(l["contadores"],"Serie"))


#Requerimiento 7

def TOPnGenero(catalog,n):
    """
    En esta función se genera un diccionario con la siguiente estructura
    dict_resultado= {"genre_1: ": {"count":#, "typeMovie":# , "typeSerie":#, "Platforms": {} }, "genre_2": {...}}
    Args:
        catalog (_type_): _description_
        n (_type_): _description_
    """
    
    
    lista=mp.valueSet(catalog["genre"])
    
    sorted_list=mg.sort(lista, cmpGenero)
    sub_list=lt.subList(sorted_list, 1,n)
    
        
    return sub_list,lt.size(sorted_list)

def cmpGenero(elemento1,elemento2):
    contador_general1=me.getValue(mp.get(elemento1["contadores"],"contenido_total"))
    contador_general2=me.getValue(mp.get(elemento2["contadores"],"contenido_total"))
    return contador_general1>contador_general2

def complementTOPnGenero(s,estructura_datos, i):
    """
    En esta función se analiza un elemento en específico y se asignan 
    los valores a la tabla hash hecha previamente
    """
    
    #Primero analizo el tipo (si serie o película)
    if i["type"]=="Movie":
        estructura_datos[s]["typeMovie"]+=1
    elif i["type"]=="TV Show":
        estructura_datos[s]["typeSerie"]+=1
    #Si es otro no lo tengo en cuenta!

    #A partir de acá analizo el tipo de plataforma
    platform = i["platform"]
    estructura_datos[s]["Platforms"][platform]+=1
    

# Funciones utilizadas para comparar elementos dentro de una lista


# ======================= CARGA DE DATOS =============================

#Esta funcion se encarga de comparar si los conetenisods de dos peliculas se dividen entre los de release year y 
#en caso de ser iguales se compare por titulo hace parte de la carga de datos carga de datos. 

def cmpByReleaseYear(content1, content2):
    """
    Devuelve verdadero (True) si el release_year de movie1 son menores que los
    de movie2, en caso de que sean iguales tenga en cuenta el titulo y en caso de que
    ambos criterios sean iguales tenga en cuenta la duración, de lo contrario devuelva
    falso (False).
    Args:
    movie1: informacion de la primera pelicula que incluye sus valores 'release_year',
    ‘title’ y ‘duration’
    movie2: informacion de la segunda pelicula que incluye su valor 'release_year',
    ‘title’ y ‘duration’
    """

    if float(content1["release_year"]) < float(content2["release_year"]):
        return True
    elif float(content1["release_year"]) == float(content2["release_year"]):
        a=(content1['title'].lower().strip()) 
        b=(content2["title"].lower().strip())
        return a<b
    
    else: 
        return False
    
def cmpreq4(content1,content2):
    if float(content1["release_year"]) < float(content2["release_year"]):
        return True
    elif float(content1["release_year"]) == float(content2["release_year"]):
        a=(content1['title'].lower().strip()) 
        b=(content2["title"].lower().strip())
        if a < b:
            return True
        elif  a == b:
            return int(content1["duration"]) < int(content2["duration"])

    else:
        return False



def cmpBytitle(content1,content2):

    """
    Devuelve True si el titulo del contenido 1 son menores que el titulo del segundo contenido,
    en caso de ser iguales se debe dirigir a comprarar las duraciones de los 2 contenidos, y en 
    caso de que sea igual se pone false.

    Args:
        content1 (_type_): Información de la primera pelicula o serie comparando el titulo y duración
        content2 (_type_): Información de la segunda pelicula o serie comparando el titulo y duración
    """
    a=(content1['title'].lower().strip()) 
    b=(content2["title"].lower().strip())
    if a < b:
        return True
    elif  a == b:
        return int(content1["duration"]) < int(content2["duration"])

    else:
        return False


# Funciones de ordenamiento

def mergesortyear(catalog):
    #start_time= getTime()
    sorted_list = mg.sort(catalog, cmpByReleaseYear)
    #end_time = getTime()
    #delta_time = deltaTime(start_time, end_time)
    return sorted_list


#Funciones para llevar el tiempo

def getTime():
    return float(time.perf_counter() * 1000)

def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Códigos de mirar cuales son los 3 primeros y los 3 ultimos de la lista que se le pase, creando una sublista

def primeros_3a(catalog):
    return (lt.subList(catalog, 1, 3))

def ultimos(catalog):
    return lt.subList(catalog,-3,3)
