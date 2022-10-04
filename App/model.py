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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
assert cf


# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    
    catalog = {'mix': None,
               'listed_in': None}

    catalog['mix'] = lt.newList('ARRAY_LIST', cmpMoviesByReleaseYear)
    catalog['nf'] = lt.newList('ARRAY_LIST', cmpMoviesByReleaseYear)
    catalog['am'] = lt.newList('ARRAY_LIST', cmpMoviesByReleaseYear)
    catalog['hl'] = lt.newList('ARRAY_LIST', cmpMoviesByReleaseYear)
    catalog['dy'] = lt.newList('ARRAY_LIST', cmpMoviesByReleaseYear)

    catalog['listed_in'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=10,
                                   comparefunction=None)
    catalog['release_year'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=10,
                                   comparefunction=None)
    catalog['date_added'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=10,
                                   comparefunction=None)
    catalog['cast'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=10,
                                   comparefunction=None)
    catalog['country'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=None)
    catalog['director'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=10,
                                   comparefunction=None)
    return catalog


# Funciones para agregar informacion al catalogo

def addMovie(catalog, book,plat,plat2=''):
    book['stream_service'] = plat2
    lt.addLast(catalog[plat], book)
    
    return catalog

def addMovieMap(catalog, book):
    #Req 4 Generos
    genero=book["listed_in"]
    if ',' in genero:
        generos=genero.split(', ')
        for i in generos:
            addMovieMap2(catalog,i,book,'listed_in') 
    else:
        addMovieMap2(catalog,genero,book,'listed_in')
    
    #Req 5 Paises
    pais=book["country"]
    if ',' in pais:
        paises=pais.split(', ')
        for i in paises:
            addMovieMap2(catalog,i,book,'country') 
    else:
        addMovieMap2(catalog,pais,book,'country')
    
    #Req 6 Director
    director=book["director"]
    if ',' in director:
        directores=director.split(', ')
        for i in directores:
            addMovieMap2(catalog,i,book,'director') 
    else:
        addMovieMap2(catalog,director,book,'director')
   
    return catalog


def addMovieMap2(catalog, pais, book, req):
    exist = mp.contains(catalog[req], pais)
    if exist:
        dicci = mp.get(catalog[req], pais)
        value = me.getValue(dicci)
    else:
        value = newThing()
        mp.put(catalog[req], pais, value)
    lt.addLast(value['books'], book)


# Funciones para creacion de datos

def newThing():
    thing = {
              "books": None
              }
    thing['books'] = lt.newList('ARRAY_LIST')
    return thing

# Funciones de consulta

def titleSize(catalog,plat):
    return lt.size(catalog[plat])

def getPrimeros(catalog, number,plat):
    movies = catalog[plat]
    bestmovies = lt.newList()
    for cont in range(1, number+1):
        movie = lt.getElement(movies, cont)
        lt.addLast(bestmovies, movie)
    return bestmovies

def getUltimos(catalog, number,plat):
    movies = catalog[plat]
    bestmovies = lt.newList()
    for cont in range(lt.size(catalog[plat]), lt.size(catalog[plat])-number,-1):
        movie = lt.getElement(movies, cont)
        lt.addLast(bestmovies, movie)
    return bestmovies

def getReq5(catalog, pais):
    start_time=getTime()
    movies = mp.get(catalog['country'], pais)
    movies = me.getValue(movies)['books']
    movies_pais_TV=lt.newList('ARRAY_LIST')
    movies_pais_Peli=lt.newList('ARRAY_LIST')
    for i in lt.iterator(movies): 
        if i['type']=='TV Show':
            lt.addLast(movies_pais_TV, i)
        elif i['type']=='Movie':
            lt.addLast(movies_pais_Peli, i)
    mer.sort(movies_pais_TV, cmpMoviesByReleaseYear)
    mer.sort(movies_pais_Peli, cmpMoviesByReleaseYear)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    print(movies_pais_TV)
    return movies_pais_TV, movies_pais_Peli,round(times,3)

def getReq6(catalog, director):
    start_time=getTime()
    peliculas= mp.get(catalog['director'], director)
    peliculas= me.getValue(peliculas)['books']

    num_todo_director= lt.size(peliculas)
    
    mer.sort(peliculas, cmpMoviesByReleaseYear)

    num_movies_director= 0
    num_shows_director=0
    numero_generos_autordic={}
    plataformasdic={}

    for cont in lt.iterator(peliculas):

        plat=cont["stream_service"]
        if plat in plataformasdic:
            plataformasdic[plat]+=1
        else:
            plataformasdic[plat]=1

        if cont["type"] =="Movie":
            num_movies_director+=1
        elif cont["type"] =="TV Show":
            num_shows_director=+1
        x=cont["listed_in"]
        if ',' in x:
            genero_x_pelicula=x.split(', ')
            for i in genero_x_pelicula:
                if i in numero_generos_autordic:
                    numero_generos_autordic[i]+=1
                else:
                    numero_generos_autordic[i]=1
    
    numero_generos_autor=[]
    for i in numero_generos_autordic:
        j=[i,numero_generos_autordic[i]]
        numero_generos_autor.append(j)

    plataformas=[]
    for i in plataformasdic:
        j=[i,plataformasdic[i]]
        plataformas.append(j)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return num_todo_director,num_movies_director, num_shows_director, numero_generos_autor, plataformas, peliculas,round(times,3)

# Funciones de ordenamiento

def cmpMoviesByReleaseYear(movie1, movie2):
    if movie1['release_year']==movie2['release_year']:
        if movie1['title'].lower() == movie2['title'].lower():
            if movie1['duration']<movie2['duration']:
                return 0
        elif movie1['title'].lower() < movie2['title'].lower():
            return 0
        else:
            return 1
    elif movie1['release_year']<movie2['release_year']:
        return 0
    else:
        return 1

#Funciones de Tiempo

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