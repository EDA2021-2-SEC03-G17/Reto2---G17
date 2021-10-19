"""
 * Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 * Reto No.2 - MoMAs
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import quicksort as qs
assert cf

# Construccion de modelos

def newCatalog():

    catalog = {'Artistas': None,
               'Obras': None,
               'Medios Obras': None,
               'Fecha': None}
               

    catalog['Artistas'] = mp.newMap(76,
                                   maptype='PROBING',
                                   loadfactor=4.0)

    catalog['Obras'] = mp.newMap(294,
                                   maptype='PROBING',
                                   loadfactor=4.0)

    catalog['Medios Obras'] = mp.newMap(maptype='CHAINING',loadfactor=0.80)

    catalog["Nacionalidad Artistas"] = mp.newMap(numelements=15225,maptype='CHAINING',loadfactor=0.80)

    catalog['Fecha'] = mp.newMap(maptype='CHAINING',loadfactor=8.0)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    
    artistas=catalog["Nacionalidad Artistas"]
    mp.put(catalog['Artistas'], int(artist["ConstituentID"]), artist)
    add_map_bynationality(artistas,artist)

def addArtwork (catalog, artwork):

    obras=catalog['Medios Obras']
    obras2=catalog["Fecha"]

    mp.put(catalog['Obras'], int(artwork["ObjectID"]), artwork)
    add_map_bymedium(obras,artwork)
    add_map_bydate(obras2, artwork)

def add_map_bymedium (obras,artwork):

    b=mp.contains(obras, artwork["Medium"])

    if b:
        if artwork["Medium"]!="":
            a=mp.get(obras,artwork["Medium"])
            a=me.getValue(a)
            lt.addLast(a,artwork)
        
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,artwork)
        mp.put(obras, artwork["Medium"],lista)

def add_map_bynationality (obras,artwork):

    b=mp.contains(obras, artwork["Nationality"])

    if b:
        if artwork["Nationality"]!="":
            a=mp.get(obras,artwork["Nationality"])
            a=me.getValue(a)
            lt.addLast(a,artwork)
        
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,artwork)
        mp.put(obras, artwork["Nationality"],lista)

def add_map_bydate(obras, artwork):

    b=mp.contains(obras, artwork["DateAcquired"])

    if b:
        if artwork["DateAcquired"]!="":
            a=mp.get(obras,artwork["DateAcquired"])
            a=me.getValue(a)
            lt.addLast(a,artwork)
        
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,artwork)
        mp.put(obras, artwork["DateAcquired"],lista)    


# Funciones para creacion de datos

# Funciones de consulta

def medioAntiguo(catalogo,num,medio):
    print(medio)#Exhibition catalogue with one loose editioned print
    medium = mp.get(catalogo["Medios Obras"], medio)
    oldartwork = lt.newList("ARRAY_LIST")
    print(medium)
    if medium:
        lt.addLast(oldartwork, me.getValue(medium))

        
    return oldartwork

def obrasNacionalidad(catalog, nacionalidad):
    existe = mp.contains(catalog["Nacionalidad Artistas"],nacionalidad)
    if existe:
        pareja = mp.get(catalog["Nacionalidad Artistas"], nacionalidad)
        list_artistas = me.getValue(pareja)
        tamaño = lt.size(list_artistas)
    return tamaño

def ArtistsSize(catalog):
    return mp.size(catalog['Artistas'])

def ArtworksSize(catalog):
    return mp.size(catalog['Obras'])

def artworksbyDate(catalog, date1, date2):
    fechas = sa.sort(mp.keySet(catalog['Fecha']),DateComparisonHigher)
    nuevo_mapa = mp.newMap(numelements=300,maptype='CHAINING',loadfactor=0.8)
    for i in range(0, lt.size(fechas)):
        fecha_especifica = lt.getElement(fechas,i)
        if DateComparisonHigher(fecha_especifica,date1) == True and DateComparisonLower(fecha_especifica,date2) == True:
           obras = mp.get(catalog['Fecha'], fecha_especifica)
           if mp.contains(nuevo_mapa, fecha_especifica) == False:
               mp.put(nuevo_mapa,fecha_especifica,me.getValue(obras))
    obras_filtradas = mp.valueSet(nuevo_mapa)
    contador = 0
    contador_purchase = 0
    for i in range(0, lt.size(obras_filtradas)):
        tamaño = lt.size(lt.getElement(obras_filtradas, i))
        contador+=tamaño
        if tamaño >= 1:
            list_obras = lt.getElement(obras_filtradas,i)
            for i in range(0,lt.size(list_obras)):
                obra_especifica = lt.getElement(list_obras,i)
                if 'Purchase' in obra_especifica['CreditLine'] or 'purchase' in obra_especifica['CreditLine']:
                    contador_purchase+=1
    x=mp.keySet(nuevo_mapa)
    qs.sort(x,DateComparisonLower)
    nueva_list = lt.newList()
    nueva_list2 = lt.newList()
    lt.addLast(nueva_list,lt.removeFirst(x))
    lt.addLast(nueva_list,lt.removeFirst(x))
    lt.addLast(nueva_list,lt.removeFirst(x))
    lt.addLast(nueva_list2,lt.removeLast(x))
    lt.addLast(nueva_list2,lt.removeLast(x))
    lt.addLast(nueva_list2,lt.removeLast(x))
    i=0
    tamaño=0
    lista_respuesta = lt.newList()
    while tamaño <=3: 
        fecha = lt.getElement(nueva_list,i)
        pareja = mp.get(nuevo_mapa,fecha)
        listadeobras = me.getValue(pareja)
        lt.addLast(lista_respuesta,listadeobras)
        i+=1
        tamaño+=lt.size(listadeobras)

    return print(lista_respuesta)

def artworksbyNationality(catalog):
    nacionalidades = catalog['Nacionalidad Artistas']
    nacionalidad_lista = mp.keySet(nacionalidades)
    mapa_nuevo =  mp.newMap(numelements=200,maptype='CHAINING',loadfactor=1)
    for i in lt.iterator(nacionalidad_lista):
        pareja = mp.get(nacionalidades,i)
        lista_obras = me.getValue(pareja)
        tamaño = lt.size(lista_obras)
        if not mp.contains(mapa_nuevo,tamaño):
            mp.put(mapa_nuevo,tamaño,i)
    grupo = sa.sort(mp.keySet(mapa_nuevo),higherLower)
    first_ten = lt.subList(grupo,0,11)
    first_ten_nationalities = lt.newList()
    for i in lt.iterator(first_ten):
        pareja = mp.get(mapa_nuevo,i)
        lt.addLast(first_ten_nationalities,pareja)
    x = mp.get(nacionalidades,'American')
    y=lt.size(me.getValue(x))
    return first_ten_nationalities


  
# Funciones utilizadas para comparar elementos dentro de una lista
def DateComparisonLower(date1, date2):
    #Determina si Date1 es menor a Date2
    State = True
    if len(date1) > 0 and len(date2) > 0:
        year_date1 = int(date1[0:4])
        year_date2 = int(date2[0:4])
        month_date1 = int(date1[5:7])
        month_date2= int(date2[5:7])
        day_date1 = int(date1[8:])
        day_date2 = int(date2[8:])
        if year_date1 > year_date2:
            State = False
        if year_date1 == year_date2:
            if month_date1 > month_date2:
                State = False
            if month_date1 == month_date2:
                if day_date1 > day_date2:
                    State = False
    else:
        State = False
    return State

def DateComparisonHigher(date1, date2):
    #Determina si Date1 es mayor a Date2
    State = True
    if len(date1) > 0 and len(date2) > 0:
        year_date1 = int(date1[0:4])
        year_date2 = int(date2[0:4])
        month_date1 = int(date1[5:7])
        month_date2= int(date2[5:7])
        day_date1 = int(date1[8:])
        day_date2 = int(date2[8:])
        if year_date1 < year_date2:
            State = False
        if year_date1 == year_date2:
            if month_date1 < month_date2:
                State = False
            if month_date1 == month_date2:
                if day_date1 < day_date2:
                    State = False
    else:
        State = False
    return State

def higherLower(num1,num2):
    return num1>num2
# Funciones de ordenamiento


