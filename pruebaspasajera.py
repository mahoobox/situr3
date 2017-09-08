from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json


archivo = open("jsontest.json","w")
leer = json.loads(urlopen('http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico').read())
cantidadResultados = str(len(leer))#Contar Cantidad de Resultados Encontrados
#range(0,len(leer))#Rango que recorre la cantidad de resultados mostrados


#EXTRAER PST
"""for x in range(0,len(leer)):
    nombre = leer[x]['name']
    slug = leer[x]['slug']
    idtag = leer[x]['id']
    print (nombre+","+str(idtag)+","+slug)
"""

#EXTRAER LISTADO ATRACTIVOS
for x in range(0,len(leer)):
    nombre = leer[x]['title']['rendered']
    print (nombre)