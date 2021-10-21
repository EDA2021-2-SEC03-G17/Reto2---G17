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
import re 
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
               'Fecha': None,
               'Identificador': None}
               

    catalog['Artistas'] = mp.newMap(76,
                                   maptype='PROBING',
                                   loadfactor=4.0)

    catalog['Obras'] = mp.newMap(138100,
                                   maptype='PROBING',
                                   loadfactor=4.0)

    catalog['Obras Artista'] = mp.newMap(15225,maptype='CHAINING',loadfactor=0.4)
    
    catalog["Nacionalidad Artistas"] = mp.newMap(numelements=15225,maptype='CHAINING',loadfactor=0.80)

    catalog['Fecha'] = mp.newMap(maptype='CHAINING',loadfactor=8.0)

    catalog['Identificador'] = mp.newMap(numelements=5000,maptype='CHAINING',loadfactor=1.0)
    
    catalog["Fecha Artistas"]=mp.newMap(maptype='CHAINING',loadfactor=0.4)

    catalog["Por Departamento"]=mp.newMap(maptype='CHAINING',loadfactor=0.4)
    
    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    
    artistas=catalog["Nacionalidad Artistas"]
    artistas_fecha=catalog["Fecha Artistas"]
    mp.put(catalog['Artistas'], artist["DisplayName"], artist)
    add_map_bynationality(artistas,artist)
    add_map_bydate(artistas_fecha,artist)

def addArtwork (catalog, artwork):

    obras=catalog['Obras Artista']
    obras2=catalog["Por Departamento"] 
    obras4=catalog['Identificador']
    obras3=catalog["Fecha"]
   
    mp.put(catalog['Obras'], int(artwork["ObjectID"]), artwork)
    add_map_bydate2(obras3, artwork)
    add_map_byID(obras4,artwork)
    add_map_byauthorID(obras,artwork)
    add_map_bydep(obras2,artwork)

def add_map_byauthorID (obras,artwork):

    dic={"TITULO ": artwork["Title"],
    "FECHA ":  artwork["Date"],
    "TECNICA ": artwork["Medium"],
    "DIMENSIONES ": artwork["Dimensions"]}

    element=artwork["ConstituentID"].strip('[]')
    element=element.split(",")

    for authorID in element:
        authorID=authorID.strip()
        b=mp.contains(obras, authorID)

        if b:
            a=mp.get(obras,authorID)
            a=me.getValue(a)
            lt.addLast(a,dic)
            
        else:
            lista=lt.newList("ARRAY_LIST")
            lt.addLast(lista,dic)
            mp.put(obras,authorID,lista)

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

def add_map_bydate(obras,artist):
    b=mp.contains(obras, artist["BeginDate"])

    artista={"Nombre":artist["DisplayName"],
    "Nacimiento":artist["BeginDate"],
    "Fallecimento":artist["EndDate"],
    "Nacionalidad":artist["Nationality"],
    "Genero":artist["Gender"]}
    
    if b:
        a=mp.get(obras,artist["BeginDate"])
        a=me.getValue(a)
        lt.addLast(a,artista)
        
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,artista)
        mp.put(obras, artist["BeginDate"],lista)

def add_map_bydate2(obras, artwork):

    b=mp.contains(obras, artwork["ConstituentID"])

    if b:
        if artwork["DateAcquired"]!="":
            a=mp.get(obras,artwork["DateAcquired"])
            a=me.getValue(a)
            lt.addLast(a,artwork)
        
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,artwork)
        mp.put(obras, artwork["DateAcquired"],lista)

def add_map_byID(obras, artwork):

    id = artwork['ConstituentID'].replace('[','').replace(']','')
    b=mp.contains(obras, id)

    if b:
        if artwork["ConstituentID"]!="":
            a=mp.get(obras,id)
            a=me.getValue(a)
            lt.addLast(a,artwork)
        
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,artwork)
        mp.put(obras, id,lista)   

def add_map_bydep(obras,artwork):

    dic={"TITULO ": artwork["Title"],
    "ARTISTA ": artwork["ConstituentID"],
    "CLASIFICACION ":artwork["Classification"],
    "FECHA ": artwork["Date"],
    "TECNICA ": artwork["Medium"],
    "DIMENSIONES ": artwork["Dimensions"],
    "MEDIDAS ": [artwork['Circumference (cm)'],artwork['Depth (cm)'],artwork['Diameter (cm)'],
    artwork['Height (cm)'],artwork['Length (cm)'],artwork['Weight (kg)'],artwork['Width (cm)'],
    artwork['Seat Height (cm)']],
    "PESO": artwork['Weight (kg)']}

    b=mp.contains(obras,artwork["Department"])

    if b:
        a=mp.get(obras,artwork["Department"])
        a=me.getValue(a)
        lt.addLast(a,dic)
        
    else:
        lista=lt.newList("ARRAY_LIST")
        lt.addLast(lista,dic)
        mp.put(obras, artwork["Department"],lista)

# Funciones para creacion de datos
def sort_by_num(a,b):
    if a!=0:
        a=int(a)
    if b!=0:
        b=int(a)
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

#REQ 1
def crono_artistas(catalog,anio_i,anio_f):
    start_time = time.process_time() 

    tam=3
    not_full=True
    FIRST=[]
    LAST=[]
    f1=[]
    dic={"PRIMEROS ARTISTAS": FIRST,
        "ULTIMOS ARTISTAS":LAST,
        "TOTAL DE ARTISTAS":0}

    for i in range(anio_i,anio_f+1):
        exists=mp.contains(catalog,str(i))
        if exists:
            f1+=[str(i)]
            if len(f1)>3:
                f1.pop(0)
            dupla=mp.get(catalog,str(i))
            valor=me.getValue(dupla)
            tamanio=lt.size(valor)
            dic["TOTAL DE ARTISTAS"]+=tamanio

            if not_full:
                
                for element in lt.iterator(valor):
                    dic["PRIMEROS ARTISTAS"].append(element)
                    tam-=1
                    if tam==0:
                        not_full=False
                        break
    if len(f1)>0:                         
        dic=get_last_3(dic,catalog,f1)
    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000

    return dic,elapsed_time_mseg
    
def get_last_3(dic,catalog,f1):
    not_full=True
    tam=3
    pos=len(f1)-1
    while not_full:
        if tam>0:        
            dupla=mp.get(catalog,f1[pos])
            valor2=me.getValue(dupla)
            for element in lt.iterator(valor2):
                dic["ULTIMOS ARTISTAS"].append(element)
                tam-=1
                if tam==0:
                    not_full=False
                    break 
            pos-=1
    return dic

#REQ 2
def artworksbyDate(catalog, date1, date2):
    fechas = sa.sort(mp.keySet(catalog['Fecha']),DateComparisonHigher)
    nuevo_mapa = mp.newMap(numelements=300,maptype='CHAINING',loadfactor=1)
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
    return 'Hay un total de: '+str(contador) + 'obras en el rango', 'Las obras compradas en ese rango fueron: ' + str(contador_purchase), lista_respuesta,

#REQ 3
def artista_tecnica(catalog,nombre):
    start_time = time.process_time() 
    exists=mp.contains(catalog["Artistas"],nombre)
    value=""

    a={"TOTALOBRAS":"NO HAY OBRAS","TOTALTECNICAS":0,
            "TECNICATOP":"","OBRAS POR LA TECNICA":0}
    dic=mp.newMap()

    if exists:
        value=mp.get(catalog["Artistas"],nombre)
        value=me.getValue(value)
        value=value["ConstituentID"]
        value=value.strip()

    exists=mp.contains(catalog["Obras Artista"],value)

    if exists:
        value=mp.get(catalog["Obras Artista"],value)
        value=me.getValue(value)
        a["TOTALOBRAS"]=lt.size(value)

        for obra in lt.iterator(value):
            exists=mp.contains(dic,obra["TECNICA "])

            if exists:
                
                b=mp.get(dic,obra["TECNICA "])
                b=me.getValue(b)
                lt.addLast(b,obra)     

            else:  

                lista=lt.newList("ARRAY_LIST")
                lt.addLast(lista,obra)
                mp.put(dic, obra["TECNICA "], lista)
    
        value=0
        key=obra["TECNICA "]
        llaves=mp.keySet(dic)
        for medio in lt.iterator(llaves):
            val=mp.get(dic,medio)
            val=me.getValue(val)
            longitud=lt.size(val)
            if longitud>=value:
                value=longitud
                key=medio
        a["TOTALTECNICAS"]=lt.size(dic)
        a["TECNICATOP"]=key
        a["OBRAS POR LA TECNICA"]=me.getValue(mp.get(dic,key))
        stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000
    return a, elapsed_time_mseg

#REQ 4
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
    return first_ten_nationalities

def firstandlast2(catalog,lst):
    map_nacionalidades = catalog['Nacionalidad Artistas']
    primera_nacionalidad = me.getValue(lt.getElement(lst,0))
    pareja_lista_obras_nacionalidad = mp.get(map_nacionalidades,primera_nacionalidad)
    lista_obras_nacionalidad = me.getValue(pareja_lista_obras_nacionalidad)
    artist_id = lt.newList()
    if lt.size(lista_obras_nacionalidad) >= 6:
        for i in range(1,4):
            obra = lt.getElement(lista_obras_nacionalidad,i)
            lt.addLast(artist_id,obra['ConstituentID'])
        for i in range(lt.size(lista_obras_nacionalidad)-2,lt.size(lista_obras_nacionalidad)+1):
            obra = lt.getElement(lista_obras_nacionalidad,i)
            lt.addLast(artist_id,obra['ConstituentID'])
    x=artworkfromanartist(catalog,artist_id)
    return x

def artworkfromanartist(catalog,lst):
    artworks = catalog['Identificador']
    lista_respuesta = lt.newList()
    x=mp.keySet(artworks)
    for i in lt.iterator(lst):
        pareja = mp.get(artworks,i)
        obra = me.getValue(pareja)
        lt.addLast(lista_respuesta,obra)
    return lista_respuesta

#REQ 5
def transporteobras(catalog,depmuseo):
    start_time = time.process_time() 
    sumattl=0
    pesottl=0
    a={"TOTAL OBRAS":0,"ESTIMADO USD":0,"PESO ESTIMADO":0,
            "OBRAS ANTIGUAS":"vacio", "OBRAS COSTOSAS":"vacio"}

    if mp.contains(catalog["Por Departamento"],depmuseo):

        info=mp.get(catalog["Por Departamento"],depmuseo)
        info=me.getValue(info)

        for obra in lt.iterator(info):
                calculos=sumasdeobras(obra)
                obra["COSTO"]=calculos
                sumattl+=calculos
                pesopieza=obra["PESO"].strip()
                if pesopieza!="":
                    pesottl+=float(pesopieza)
    
        obrasantiguas5=sa.sort(info,cmpfunction=compareold)
        obrasantiguas5=lt.subList(obrasantiguas5,1,5)

        obrascostosas=sa.sort(info,cmpfunction=compareprice)
        obrascostosas=lt.subList(obrascostosas,1,5) 

        a={"TOTAL OBRAS":lt.size(info),"ESTIMADO USD": sumattl,"PESO ESTIMADO":pesottl,
            "OBRAS ANTIGUAS":obrasantiguas5, "OBRAS COSTOSAS": obrascostosas}
    stop_time = time.process_time() 
    elapsed_time_mseg = (stop_time - start_time)*1000
    return a, elapsed_time_mseg

def sumasdeobras(obra):
    d=obra["DIMENSIONES "]
    a=48.00
    if d!= "":
        d=d.replace('x',"*")
        d=d.replace('×',"*")
        num=[float(s) for s in re.findall(r'-?\d+\.?\d*', d)]
        if len(num)==8:
            cm=num[6:8]
            a=centimeter(cm)
        elif len(num)==16:
            cm=num[6:8]
            pcm=centimeter(cm)
            cm1=num[14:16]
            pcm1=centimeter(cm1)
            a=max(pcm,pcm1)
        elif len(num)==4:
            cm=num[2:4]
            a=centimeter(cm)
        elif len(num)==6:
            cm=num[4:6]
            a=centimeter(cm)
        elif len(num)==14:
            cm=num[7:9]
            cm1=num[12:14]
            pcm=centimeter(cm)
            pcm1=centimeter(cm1)
            a=max(pcm,pcm1)
        elif len(num)==12:
            cm3=num[9:12]
            a=centimeter(cm3)
        elif len(num)==9:
            cm3=num[6:9]
            a=centimeter(cm3)
                
    return a

def centimeter(cm:list):
    costo=72.00/((cm[0]*cm[1])/100)
    return costo

def centimetercubic(cm:list):
    costo=72.00/((cm[0]*cm[1]*cm[2])/100)
    return costo

def compareprice(PRICE1,PRICE2):
    return PRICE1["COSTO"]<PRICE2["COSTO"]

def compareold(obra1,obra2):
    a=obra1["FECHA "]
    b=obra2["FECHA "]
    val=2020
    val1=2020

    if a!="":
        if (len(a)==11) or ("c" in a):
            val=(a[-4:])
        elif "-" in a:
            val=(a[:5])
        
    if b!="":
        if (len(b)==11) or ("c" in b):
            val1=(b[-4:])
        elif "-" in b:
            val1=(val[:5])
        
    return int(val)>int(val1)

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


