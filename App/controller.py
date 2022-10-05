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
import csv
import time
import tracemalloc
...
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def newController():
    """
    Crea una instancia del modelo
    """
    control = {'model': None}
    control['model'] = model.newCatalog()
    return control

# Funciones para la carga de datos

def loadData(control,archiv,memory=False):
    start_time=  getTime()

    if memory == True:
        tracemalloc.start()
        start_memory = getMemory()

    catalog = control['model']
    nf,features= loadMovieNetflix(catalog,archiv)
    am= loadMovieAmazon(catalog,archiv)
    hl= loadMovieHulu(catalog,archiv)
    dy= loadMovieDisney(catalog,archiv)

    stop_time=getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memory == True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return nf,am,hl,dy,features, delta_time, delta_memory

    else:
        return nf, am,hl,dy,features, delta_time,None


def loadMovieNetflix(catalog,archiv):
    booksfile = cf.data_dir + 'netflix_titles-utf8-'+archiv
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    plat='nf'
    for book in input_file:
        model.addMovie(catalog, book, plat)
        model.addMovie(catalog,book,'mix', 'netflix')
        model.addMovieMap(catalog,book)
        features=len(book.keys())
    #sortMovies(catalog,plat)
    return model.titleSize(catalog,plat),features

def loadMovieAmazon(catalog,archiv):
    booksfile = cf.data_dir + 'amazon_prime_titles-utf8-'+archiv
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    plat='am'
    for book in input_file:
        model.addMovie(catalog, book,plat)
        model.addMovie(catalog,book,'mix','amazon prime')
        model.addMovieMap(catalog,book)
    #sortMovies(catalog,plat)
    return model.titleSize(catalog,plat)

def loadMovieHulu(catalog,archiv):
    booksfile = cf.data_dir + 'hulu_titles-utf8-'+archiv
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    plat='hl'
    for book in input_file:
        model.addMovie(catalog, book,plat)
        model.addMovie(catalog,book,'mix','hulu')
        model.addMovieMap(catalog,book)
    #sortMovies(catalog,plat)
    return model.titleSize(catalog,plat)

def loadMovieDisney(catalog,archiv):
    booksfile = cf.data_dir + 'disney_plus_titles-utf8-'+archiv
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    plat='dy'
    for book in input_file:
        model.addMovie(catalog, book,plat)
        model.addMovie(catalog,book,'mix','disney plus')
        model.addMovieMap(catalog,book)
    #sortMovies(catalog,plat)
    return model.titleSize(catalog,plat)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getBestBooks(control, number,plat):
    bestbooks = model.getPrimeros(control['model'], number,plat)
    return bestbooks

def getLastMovies(control, number,plat):
    bestbooks = model.getUltimos(control['model'], number,plat)
    return bestbooks

def getReq1(control,ini):
    movies_pais,time=model.getReq1(control['model'],ini)
    return movies_pais,time

def getReq2(control,ini):
    movies_pais,time=model.getReq2(control['model'],ini)
    return movies_pais,time

def getReq3(control,actor):
    casting = model.getReq3(control['model'], actor)
    return casting

def getReq4(control,top):
    actor=model.getReq4(control['model'],top)
    return actor

def getReq5(control,pais):
    movies_pais=model.getReq5(control['model'],pais)
    return movies_pais

def getReq6(control, director):
    return model.getReq6(control['model'], director)

def getReq7(control,top):
    actor=model.getReq7(control['model'],top)
    return actor

# Funciones de tiempo

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
