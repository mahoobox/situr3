from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json


archivo = open("extraerjsonatxt_resultado.txt","w")
"""
#EXTRAER CATEGORÍAS (MUNICIPIOS)
leer = json.loads(urlopen('http://situr.boyaca.gov.co/wp-json/wp/v2/categories').read())
cantidadResultados = str(len(leer))#Contar Cantidad de Resultados Encontrados
for x in range(0,len(leer)):
    nombre = leer[x]['name']
    slug = leer[x]['slug']
    idtag = leer[x]['id']
    archivo.write(str((nombre) +'\n'))
    print (nombre+","+str(idtag)+","+slug)

"""
#EXTRAER ATRACTIVOS TURÍSTICOS DE SITUR
leer = json.loads(urlopen('http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico').read())
cantidadResultados = str(len(leer))#Contar Cantidad de Resultados Encontrados
for x in range(0,len(leer)):
    nombre = leer[x]['title']['rendered']
    archivo.write(str((nombre) +'\n'))
    print (nombre)
