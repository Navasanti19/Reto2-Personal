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

from datetime import datetime
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

    forma='PROBING'
    load=0.7

    catalog['listed_in'] = mp.newMap(100,
                                   maptype=forma,
                                   loadfactor=load,
                                   comparefunction=None)
    catalog['listed_in2'] = mp.newMap(100,
                                   maptype=forma,
                                   loadfactor=load,
                                   comparefunction=None)
    catalog['release_year'] = mp.newMap(100,
                                   maptype=forma,
                                   loadfactor=load,
                                   comparefunction=None)
    catalog['date_added'] = mp.newMap(100,
                                   maptype=forma,
                                   loadfactor=load,
                                   comparefunction=None)
    catalog['cast'] = mp.newMap(100,
                                   maptype=forma,
                                   loadfactor=load,
                                   comparefunction=None)
    catalog['country'] = mp.newMap(100,
                                   maptype=forma,
                                   loadfactor=load,
                                   comparefunction=None)
    catalog['director'] = mp.newMap(100,
                                   maptype=forma,
                                   loadfactor=load,
                                   comparefunction=None)
    return catalog


# Funciones para agregar informacion al catalogo

def addMovie(catalog, book,plat,plat2=''):
    book['stream_service'] = plat2
    lt.addLast(catalog[plat], book)
    
    return catalog

def addMovieMap(catalog, book):
    #Req 1 Anio Release
    anio=book["release_year"]
    addMovieMap2(catalog,anio,book,"release_year")
    
    #Req 2 Anio Added
    if book["date_added"]!='':
        anio=str(datetime.strptime(book["date_added"], "%B %d, %Y"))
        addMovieMap2(catalog,anio,book,"date_added")
    else:
        anio=book["date_added"]
        addMovieMap2(catalog,anio,book,"date_added")
    
    #Req 3 Cast
    genero=book["cast"]
    if ',' in genero:
        generos=genero.split(', ')
        for i in generos:
            addMovieMap2(catalog,i,book,'cast')
    elif genero=='':
        addMovieMap2(catalog,'Unknown',book,'cast')
    else:
        addMovieMap2(catalog,genero,book,'cast')

    #Req 4 Generos
    genero=book["listed_in"]
    if ',' in genero:
        generos=genero.split(', ')
        for i in generos:
            if '&' in i:
                j=i.split(' & ')
                for k in j:
                    addMovieMap2(catalog,k,book,'listed_in')
            
            addMovieMap2(catalog,i,book,'listed_in') 
    else:
        if '&' in genero:
            j=genero.split(' & ')
            for k in j:
                addMovieMap2(catalog,k,book,'listed_in')
        
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
   
    #Req 7 Generos
    genero=book["listed_in"]
    if ',' in genero:
        generos=genero.split(', ')
        for i in generos:      
            addMovieMap2(catalog,i,book,'listed_in2') 
    else:
        addMovieMap2(catalog,genero,book,'listed_in2')
    
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
    value['count']+=1


# Funciones para creacion de datos

def newThing():
    thing = {
              "books": None,
              "count": 0
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

def getReq1(catalog,f_ini):
    start_time=getTime()
    movies = mp.get(catalog['release_year'], f_ini)
    movies = me.getValue(movies)['books']
    movies2=lt.newList('ARRAY_LIST')
    for i in lt.iterator(movies): 
        if i['type']=='Movie':
            lt.addLast(movies2, i)
    mer.sort(movies2, cmpMoviesByTitle)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return movies2,round(times,3)

def getReq2(catalog,f_ini):
    start_time=getTime()
    movies = mp.get(catalog['date_added'], f_ini)
    movies = me.getValue(movies)['books']
    movies2=lt.newList('ARRAY_LIST')
    for i in lt.iterator(movies): 
        if i['type']=='TV Show':
            lt.addLast(movies2, i)
    mer.sort(movies2, cmpMoviesByTitle)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return movies2,round(times,3)

def getReq3(catalog, actor):
    start_time=getTime()
    movies = mp.get(catalog['cast'], actor)
    movies = me.getValue(movies)['books']
    numero_peliculas = 0
    numero_shows = 0
    for i in lt.iterator(movies):
    
        if i["type"] == "Movie":
            numero_peliculas += 1
        else:
            numero_shows += 1
    mer.sort(movies, cmpMoviesByReleaseYear)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return movies, numero_peliculas, numero_shows, round(times,3)

def getReq4(catalog,genero):
    start_time=getTime()
    peliculas= mp.get(catalog['listed_in'], genero)
    peliculas= me.getValue(peliculas)['books']
    num_peliculas_genero= 0
    num_shows_genero= 0
    for cont in lt.iterator(peliculas):
        if cont["type"] =="Movie":
            num_peliculas_genero+= 1
        else:
            num_shows_genero+=1
    mer.sort(peliculas, cmpMoviesByReleaseYear)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return  num_peliculas_genero, num_shows_genero, peliculas,round(times,3)

def getReq5(catalog, pais):
    start_time=getTime()
    movies = mp.get(catalog['country'], pais)
    movies = me.getValue(movies)['books']
    moviesTV=0
    moviesPeli=0
    for i in lt.iterator(movies): 
        if i['type']=='TV Show':
            moviesTV+=1
        else:
            moviesPeli+=1
    mer.sort(movies, cmpMoviesByReleaseYear)
    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return movies,moviesTV, moviesPeli,round(times,3)

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

def getReq7(catalog, top):
    start_time=getTime()
    #movies1=catalog['mix']
    generos=mp.keySet(catalog['listed_in2'])
    generos_cuenta=mp.valueSet(catalog['listed_in2'])
    
    lista_cuenta=lt.newList('ARRAY_LIST')
    
    for i in range(1,lt.size(generos)+1):
        lt.addLast(lista_cuenta,[lt.getElement(generos,i),lt.getElement(generos_cuenta,i)['count']])
    mer.sort(lista_cuenta,cmpByCantidad)
    top_n=lt.subList(lista_cuenta,1,top)
    info_genero={}
    for i in lt.iterator(top_n):
        movies1= mp.get(catalog['listed_in2'], i[0])
        movies1= me.getValue(movies1)['books']
        for j in lt.iterator(movies1):
            if i[0] in j['listed_in']:
                if i[0] in info_genero.keys():
                    info_genero[i[0]][j['stream_service']]+=1
                    info_genero[i[0]][j['type']]+=1
                else:
                    info_genero[i[0]]={'Movie':0,'TV Show':0,'netflix':0,'amazon prime':0,'hulu':0,'disney plus':0}
                    info_genero[i[0]][j['stream_service']]+=1
                    info_genero[i[0]][j['type']]+=1
                    
    end_time=getTime()
    times=deltaTime(start_time,end_time)            
    return lista_cuenta, info_genero, round(times,3)

def getReq8(catalog,top):
    start_time=getTime()
    movies=catalog['mix']
    lista_cuenta=lt.newList('ARRAY_LIST')
    cuenta={}
    for i in lt.iterator(movies):
        actor=i['cast']
        if actor=='':
            if 'Unknown' in cuenta.keys():
                cuenta['Unknown']+=1
            else:
                cuenta['Unknown']=1
        elif ',' in actor:
            lista_actores=actor.split(', ')
            for i in lista_actores:
                if i in cuenta.keys():
                    cuenta[i]+=1
                else:
                    cuenta[i]=1
        else:
            if actor in cuenta.keys():
                cuenta[actor]+=1
            else:
                cuenta[actor]=1
    for i in cuenta:
        lt.addLast(lista_cuenta,[i,cuenta[i]])
    mer.sort(lista_cuenta,cmpByCantidad)


    top_n=lt.subList(lista_cuenta,1,top)
    info_actores={}
    for i in lt.iterator(top_n):
        listica_colab=[]
        listica_colab_direct=[]
        actorsito= mp.get(catalog['cast'], i[0])
        actorsito= me.getValue(actorsito)['books']
        for j in lt.iterator(actorsito):
            if i[0] in info_actores.keys():
                if j['type']=='Movie':
                    lt.addLast(info_actores[i[0]]['movies'],j)
                else:
                    lt.addLast(info_actores[i[0]]['tvshow'],j)
                
                if ',' in j['listed_in']:
                    lista_genero=j['listed_in'].split(', ')
                    for k in lista_genero:
                        if k in info_actores[i[0]]['genero']:
                            info_actores[i[0]]['genero'][k]+=1
                        else:
                            info_actores[i[0]]['genero'][k]=1
                else:
                    if j['listed_in'] in info_actores[i[0]]['genero']:
                        info_actores[i[0]]['genero'][j['listed_in']]+=1
                    else:
                        info_actores[i[0]]['genero'][j['listed_in']]=1 

                info_actores[i[0]][j['stream_service']][j['type']]+=1
                info_actores[i[0]][j['type']]+=1

                if ',' in j['cast']:
                    lista_colab=j['cast'].split(', ')
                    for k in lista_colab:
                        if k not in listica_colab:
                            listica_colab.append(k)  
                else:
                    if j['cast']!='':
                        listica_colab.append(j['cast'])
                    elif 'Unknown' not in listica_colab:
                        listica_colab.append('Unknown')
                
                if ',' in j['director']:
                    lista_colab_direct=j['director'].split(', ')
                    for k in lista_colab_direct:
                        if k not in listica_colab_direct:
                            listica_colab_direct.append(k)
                else:
                    if j['director']!='' and  j['director'] not in listica_colab_direct :
                        listica_colab_direct.append(j['director'])
                    elif 'Unknown' not in listica_colab_direct:
                        listica_colab_direct.append('Unknown')
            
            else:
                info_actores[i[0]]={'genero':{},
                'netflix':{'TV Show':0,'Movie':0},
                'amazon prime':{'TV Show':0,'Movie':0},
                'hulu':{'TV Show':0,'Movie':0},
                'disney plus':{'TV Show':0,'Movie':0},
                'colaborations':'',
                'Movie':0,
                'TV Show':0,
                'direct_colab':'',
                'movies':lt.newList('ARRAY_LIST'),
                'tvshow':lt.newList('ARRAY_LIST')}
                
                if j['type']=='Movie':
                    lt.addLast(info_actores[i[0]]['movies'],j)
                else:
                    lt.addLast(info_actores[i[0]]['tvshow'],j)

                info_actores[i[0]][j['stream_service']][j['type']]+=1
                info_actores[i[0]][j['type']]+=1
                
                if ',' in j['cast']:
                    lista_colab=j['cast'].split(', ')
                    for k in lista_colab:
                        if k not in listica_colab:
                            listica_colab.append(k)  
                else:
                    if j['cast']!='':
                        listica_colab.append(j['cast'])
                    elif 'Unknown' not in listica_colab:
                        listica_colab.append('Unknown')
                
                if ',' in j['director']:
                    lista_colab_direct=j['director'].split(', ')
                    for k in lista_colab_direct:
                        if k not in listica_colab_direct:
                            listica_colab_direct.append(k)
                else:
                    if j['director']!='' and  j['director'] not in listica_colab_direct :
                        listica_colab_direct.append(j['director'])
                    elif 'Unknown' not in listica_colab_direct:
                        listica_colab_direct.append('Unknown')
        
        mer.sort(info_actores[i[0]]['movies'],cmpMoviesByReleaseYear)
        mer.sort(info_actores[i[0]]['tvshow'],cmpMoviesByReleaseYear)
        esta=True
        while esta:
            if i[0] in listica_colab and i[0]!='Unknown':
                listica_colab.remove(i[0])
                if len(listica_colab)==0:
                    listica_colab.append('No Colabora con Nadie')
            else:
                esta=False
        listica_colab.sort()
        listica_colab_direct.sort()
        
        for colab in listica_colab:
            if info_actores[i[0]]['colaborations']=='':
                info_actores[i[0]]['colaborations']=colab
            else:
                info_actores[i[0]]['colaborations']=info_actores[i[0]]['colaborations']+', '+colab
            if len(info_actores[i[0]]['colaborations'])>400:
                info_actores[i[0]]['colaborations']=info_actores[i[0]]['colaborations']+'... '
                break
        for colab in listica_colab_direct:
            if info_actores[i[0]]['direct_colab']=='':
                info_actores[i[0]]['direct_colab']=colab
            else:
                info_actores[i[0]]['direct_colab']=info_actores[i[0]]['direct_colab']+', '+colab
            if len(info_actores[i[0]]['direct_colab'])>400:
                info_actores[i[0]]['direct_colab']=info_actores[i[0]]['direct_colab']+'... '
                break

    end_time=getTime()
    times=deltaTime(start_time,end_time)
    return lista_cuenta, info_actores, round(times,3)


# Funciones de ordenamiento

def cmpMoviesByReleaseYear(movie1, movie2):
    if movie1['release_year']==movie2['release_year']:
        if movie1['title'].lower() == movie2['title'].lower():
            if movie1['duration']<movie2['duration']:
                return 0
        elif movie1['title'].lower() < movie2['title'].lower():
            return 1
        else:
            return 0
    elif movie1['release_year']<movie2['release_year']:
        return 0
    else:
        return 1

def cmpMoviesByTitle(movie1, movie2):
    if movie1['title'].lower()==movie2['title'].lower():
        if movie1['release_year'] == movie2['release_year']:
            if movie1['director'] < movie2['director']:
                return 1
        elif movie1['release_year'] < movie2['release_year']:
            return 1
        else:
            return 0
    elif movie1['title'].lower()<movie2['title'].lower():
        return 1
    else:
        return 0

def cmpMoviesByDateAdded(movie1, movie2):
    try:
        if datetime.strptime(movie1['date_added'],"%Y-%m-%d")==datetime.strptime(movie2['date_added'],"%Y-%m-%d"):
            if movie1['title'].lower() == movie2['title'].lower():
                if movie1['duration']<movie2['duration']:
                    return 0
                else:
                    return 1
            elif movie1['title'].lower() < movie2['title'].lower():
                return 0
            else:
                return 0
        elif datetime.strptime(movie1['date_added'],"%Y-%m-%d")<datetime.strptime(movie2['date_added'],"%Y-%m-%d"):
            return 0
        else:
            return 1
    except:
        if movie1['date_added']=='':
            return 1
        elif movie2['date_added']=='':
            return 0
        else: 
            return 1 

def cmpByCantidad(actor1,actor2):
    if actor1[1]>actor2[1]:
        return 1
    elif actor1[1]==actor2[1]:
        if actor1[0]>actor2[0]:
            return 1
        else:
            return 0
    else:
        return 0

#Funciones de Tiempo

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
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