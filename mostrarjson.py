from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json



buscasitur = str(input("Ingrese el atractivo que desea buscar:   "))
buscasitur_sin_espacio = buscasitur.replace(" ", "%20")
print (buscasitur_sin_espacio)

leer = json.loads(urlopen('http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?search=' + buscasitur_sin_espacio).read())
test = leer[0].get('link')

print (" ")

print ("Título del atractivo:    " + leer[0]['title']['rendered'])
print ("Url del atractivo:       " + leer[0]['link'])
print ("Ciudad del atractivo:    " + leer[0]['ciudad'])
print ("Excerpt del atractivo:   " + leer[0]['excerpt']['rendered'])
print (" ")
print (test)
