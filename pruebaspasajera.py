from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json



leer = json.loads(urlopen('http://situr.boyaca.gov.co/wp-json/wp/v2/tags/').read())
cantidadResultados = str(len(leer))#Contar Cantidad de Resultados Encontrados
#range(0,len(leer))#Rango que recorre la cantidad de resultados mostrados
name = leer[0].get('name')
slug = leer[0].get('slug')
idtag = leer[0].get('id')


print (cantidadResultados)
print (name)
print (slug)
print (idtag)

for x in range(0,len(leer)):
    nombre = leer[x]['name']
    slug = leer[x]['slug']
    idtag = leer[x]['id']
    print (nombre+","+str(idtag)+","+slug)


