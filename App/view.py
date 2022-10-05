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

from datetime import datetime
import config as cf
import sys
import controller
from tabulate import tabulate
import os
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# Funciones de Print

def printMovies(movies):
    size = lt.size(movies)
    if size:
        headers = [list(movies['first']['info'].keys())]
        table=[]
        for movie in lt.iterator(movies):
            table.append([movie['show_id'],movie['type'],movie['title'],movie['director'],movie['cast'],movie['country'],movie['date_added'],movie['release_year'],movie['rating'],movie['duration'],movie['listed_in'],movie['description'],movie['stream_service']])
        print(tabulate(table,headers[0],tablefmt="grid",maxcolwidths=14))    
        print('\n')    
    else:
        print('No se encontraron peliculas')

def printMoviesCant(movies,cant,head):
    size = lt.size(movies)
    if size:
        
        table=[]
        i=1
        for movie in lt.iterator(movies):
            headers = []
            for j in range(len(head)):
                headers.append(movie[head[j]])
            table.append(headers)
            if i==cant:
                break
            else:
                i+=1
        if size>=cant*2:
            i=0
            for movie in lt.iterator(movies):
                headers = []
                if size-i<=cant:
                    for j in range(len(head)):
                        headers.append(movie[head[j]])
                    table.append(headers)
                if size-i==0:
                    break
                else:
                    i+=1
        print(tabulate(table,head,tablefmt="grid",maxcolwidths=14))    
        print('\n')

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cosultar contenido estrenado en un año")
    print("3- Cosultar contenido añadido en un año")
    print("4- Cosultar contenido por actor")
    print("5- Cosultar contenido por género")
    print("6- Cosultar contenido por país")
    print("7- Cosultar contenido por director involucrado")
    print("8- Cosultar el Top x de los géneros con más contenido")
    print("9- el Top x de los actores con más participación")
    print("0- Salir")

# Función crear controlador

def newController():
    control = controller.newController()
    return control

# Función Cargar Datos

def loadData(control,archiv,memory):
    movies= controller.loadData(control,archiv,memory)
    return movies

# Funciones Ejecutar opciones del menú

def playLoadData():
    print('\nCuántos datos desea cargar?')
    print('1: 0.5% de los datos')
    print('2: 5% de los datos')
    print('3: 10% de los datos')
    print('4: 20% de los datos')
    print('5: 30% de los datos')
    print('6: 50% de los datos')
    print('7: 80% de los datos')
    print('8: 100% de los datos')
    resp=int(input())
    if resp==1:
        archiv='small.csv'
    elif resp==2:
        archiv='5pct.csv'
    elif resp==3:
        archiv='10pct.csv'
    elif resp==4:
        archiv='20pct.csv'
    elif resp==5:
        archiv='30pct.csv'
    elif resp==6:
        archiv='50pct.csv'
    elif resp==7:
        archiv='80pct.csv'
    elif resp==8:
        archiv='large.csv'
    
    resp=input(('\nDesea Conocer la memoria utilizada? '))
    resp=castBoolean(resp)
    nf,am,hl,dy,features,time,memory= loadData(catalog,archiv,resp)
    os.system('cls')
    print('----------------------------------')
    print('Loaded straming service info: ')
    print('Total loaded titles: '+str(nf+am+hl+dy))
    print('Total features loaded: '+str(features))
    print('----------------------------------')
    table = [["Netflix",nf],["Amazon",am],["Disney",dy],['Hulu',hl]]
    headers = ["Stream Service", "Count"]
    print(tabulate(table, headers, tablefmt="grid"))
    print('\n------ Content per stream service sorted by title ------')
    plats=['nf','am','dy','hl']
    plats_nombres=['Netflix','Amazon Prime','Disney Plus','Hulu']
    for i in range(4):
        print(f'\n{plats_nombres[i]}')
        print('First 3:')
        firstmovies = controller.getBestBooks(catalog, 3,plats[i])
        printMovies(firstmovies)
        print('Last 3:')
        lastmovies = controller.getLastMovies(catalog, 3,plats[i])
        printMovies(lastmovies)
    print(f'Tiempo de ejecución: {time:.3f}')
    print(f'Memoria Utilizada: {memory}')

def playReq1():
    anio=input('\nIngrese el año: ')
    Peli,time = controller.getReq1(catalog, anio)
    #os.system('cls')
    print('============ Req No. 1 Inputs ============')
    print(f'Movie released in the year: {anio}')

    print('\n============ Req No. 1 Answer ============')
    print(f'There are {lt.size(Peli)} IPs (Intelectual Properties) in "Movie" type released in the year {anio}')
    print('The first 3 and last 3 IPs in range are:')
    head=['type','release_year','title','duration','stream_service','director','cast']
    printMoviesCant(Peli,3,head) if lt.size(Peli)>0 else print(f'No hay peliculas estrenadas en {anio}')
    print('Tiempo de ejecución:',time,'ms\n')

def playReq2():
    anio=datetime.strptime(input('\nIngrese la fecha: '), "%B %d, %Y")
    print(anio)
    Tv, time = controller.getReq2(catalog, str(anio))
    os.system('cls')
    print('============ Req No. 2 Inputs ============')
    print(f'"TV Show" released in the date: {str(anio)[:10]}')

    print('\n============ Req No. 2 Answer ============')
    print(f'There are {lt.size(Tv)} IPs (Intelectual Properties) in the date: {str(anio)[:10]}')
    print('The first 3 and last 3 IPs in range are:')
    head=['type','date_added','title','duration','release_year','stream_service','director','cast']
    printMoviesCant(Tv,3,head) if lt.size(Tv)>0 else print(f'No hay contenido en el año {datetime.strftime(anio, "%Y-%m-%d")}')
    print('Tiempo de ejecución:',time,'ms\n')

def playReq3():
    casting = input("\nIngrese el nombre del actor que desea buscar: ")
    info_actor,a,b,timesito = controller.get11Req3(catalog, casting)
    os.system('cls')
    print('============ Req No. 3 Inputs ============')
    print(f'Content with {casting} in the "cast"')
    
    print('\n============ Req No. 3 Answer ============')
    print(f'------ "{casting}" cast participation count ------')
    numero_peliculas_y_shows = [["Movie",a],["TV Show",b]]
    print(tabulate(numero_peliculas_y_shows,['type','count'],tablefmt='grid'))
    
    print(f'\n------ Participation Detalis ------')
    print(f'There are less than 6 participation of "{casting}" on record') if lt.size(info_actor)<6 else print(f'The first 3 and last 3 IPs of "{casting}" are:')
    headers = ['release_year','title','duration','director','stream_service','type','cast','country','rating','listed_in','description']
    printMoviesCant(info_actor,3,headers) if lt.size(info_actor)>0 else print(f'No hay peliculas del actor {casting}')
    print(f'\nEl tiempo de ejecución es: {timesito} ms\n')

def playReq4():
    generodeseado = input("\nDigita el género: ")
    num_movies, num_shows,todas,timesito= controller.getReq4(catalog, generodeseado)
    os.system('cls')
    print('============ Req No. 4 Inputs ============')
    print(f'The content is "listed_in" {generodeseado}')
    
    print('\n============ Req No. 4 Answer ============')
    print(f'------ "{generodeseado}" content type count ------')
    numero_peliculas_y_shows = [["Movie",num_movies],["TV Show",num_shows]]
    print(tabulate(numero_peliculas_y_shows,['type','count'],tablefmt='grid'))

    print(f'\n------ Content Detalis ------')
    print(f'There are {lt.size(todas)} IPs (Intelectual Properties) with the {generodeseado} label')
    print(f'There are less than 6 "listed_in" {generodeseado} on record') if lt.size(todas)<6 else print(f'The first 3 and last 3 IPs in range are:')
    head=['release_year','title','duration','stream_service','director','type','cast','country','rating','listed_in','description']
    printMoviesCant(todas,3,head) if lt.size(todas)>0 else print(f'No hay peliculas del genero {generodeseado}')
    print(f'\nEl tiempo de ejecución es: {timesito} ms\n')

def playReq5():
    pais=input('Ingrese el país a consultar Ej. "United States": ')
    movies, TV,Peli,time = controller.getReq5(catalog, pais)
    os.system('cls')
    print('============ Req No. 5 Inputs ============')
    print(f'The content produced in the "{pais}"')
    
    print('\n============ Req No. 5 Answer ============')
    print(f'------ "{pais}" content type production count ------')
    table = [["Movies",Peli],["TV Show",TV]]
    headers = ["Type", "Count"]
    print(tabulate(table, headers, tablefmt="grid"))

    print('\n------ Content details ------')
    print(f'There are less than 6 produced in "{pais}" on record') if (lt.size(movies))<6 else print(f'The first 3 and last 3 IPs in produced in "{pais}" are:')

    head=['release_year','title','duration','stream_service','director','type','cast','country','rating','listed_in','description']
    printMoviesCant(movies,3,head) if lt.size(movies)>0 else print(f'There are not content in {pais}')
    print('Tiempo de ejecución:',time,'ms')

def playReq6():
    director = input("Digita el director: ")
    num_todo_director,num_movies_director, num_shows_director, numero_generos_autor, plataformas, filtro_director,timesito= controller.getReq6(catalog, director)
    os.system('cls')
    print('============ Req No. 6 Inputs ============')
    print(f'Find the content with "{director}" as ""director" ')
    
    print('\n============ Req No. 6 Answer ============')
    print(f'------ "{director}" Content type count ------')
    headers=["Type", "Count"]
    table1=[["Movies",num_movies_director],["Shows",num_shows_director]]
    print(tabulate(table1, headers, tablefmt="grid"))

    print(f'\n------ "{director}" Streaming content type count ------')
    headers2=["Service_name", "movie"]
    print(tabulate(plataformas,headers2,tablefmt="grid",maxcolwidths=18))

    print(f'\n------ "{director}" Listed in count ------')
    print("There are only", len(numero_generos_autor),"tags ib 'listed_in'")
    print('The first 3 and last 3 tags in range are:')
    headers3=['listed_in','count']
    print(tabulate(numero_generos_autor,headers3,tablefmt='grid'))
    
    print(f'\n------ "{director}" content details ------')
    print("There are only", num_todo_director, "IPs (Intelectual Properties) with", director, "as director")
    print('The first 3 and last 3 tags in range are:')
    printMoviesCant(filtro_director,3,['release_year','title','duration','director','stream_service','type','cast','country', 'rating','listed_in','description'])
    print(f'\nEl tiempo de ejecución es: {timesito} ms\n')

def playReq7():
    top_n=int(input('Que top desea consultar: '))
    cuenta_actores,info_actores,timesito=controller.getReq7(catalog,top_n)
    
    #os.system('cls')
    print('============ Req No. 7 Inputs ============')
    print(f'the TOP "{top_n}" genres in "listed_in" ')
    
    print('\n============ Req No. 7 Answer ============')
    print(f'There are "{lt.size(cuenta_actores)}" tags participating for the TOP {top_n} genres for "listed_in"')

    print(f'\n------ The TOP "{top_n}" listed_in tags are: ------')
    print(f'The TOP "{top_n}" actors are:')
    table = []
    for i in range(top_n):
        table.append([cuenta_actores['elements'][i][0],cuenta_actores['elements'][i][1]])
    headers = ["Listed_in", "Count"]
    print(tabulate(table, headers, tablefmt="grid"))

    print(f'\n------ Top actors participations details: ------')
    print(f'The TOP "{top_n}" actors are:')
    headers2 = ["type", 'count']
    headerspro=['rank','listed_in','count','type','stream_service']
    headers3=['stream_service','count']
    
    tablepro=[]
    k=1
    for i in info_actores.keys():
        table2=[]
        table3=[]
        table2.append(['Movie',info_actores[i]['Movie']])
        table2.append(['TV Show',info_actores[i]['TV Show']])
        table3.append(['netflix',info_actores[i]['netflix']])
        table3.append(['amazon',info_actores[i]['amazon prime']])
        table3.append(['hulu',info_actores[i]['hulu']])
        table3.append(['disney',info_actores[i]['disney plus']])
        tablepro.append([k,i,cuenta_actores['elements'][k-1][1],tabulate(table2,headers2,tablefmt='plain'),tabulate(table3,headers3,tablefmt='plain')])
        k+=1
    print(tabulate(tablepro,headerspro,tablefmt='grid'))
    print(f'\nEl tiempo de ejecución es: {timesito} ms\n')

# Funciones Auxiliares

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = newController()
        playLoadData() 
    elif int(inputs[0])==2:
        playReq1()
    elif int(inputs[0])==3:
        playReq2()
    elif int(inputs[0])==4:
        playReq3()
    elif int(inputs[0])==5:
        playReq4()
    elif int(inputs[0])==6:
        playReq5()
    elif int(inputs[0])==7:
        playReq6()
    elif int(inputs[0])==8:
        playReq7()
        
    else:
        sys.exit(0)



