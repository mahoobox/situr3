from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json

buscasitur = str(input("Ingrese el atractivo que desea buscar:   "))
#buscasitur = "laguna de tota"
buscasitur_sin_espacio = buscasitur.replace(" ", "%20")
print (buscasitur_sin_espacio)

leer = json.loads(urlopen('http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?search=' + buscasitur_sin_espacio).read())
cantidadResultados = str(len(leer))#Contar Cantidad de Resultados Encontrados
range(0,len(leer))#Rango que recorre la cantidad de resultados mostrados

test = leer[0].get('link')
test2 = leer[0]['title']['rendered']#Esta muestra el título 
descripcion = re.sub("<.*?>", "", leer[0]['excerpt']['rendered'])

#idJsonImagen = str(2739)
idJsonImagen = str(leer[0]['featured_media'])
leerImagen = json.loads(urlopen('http://www.situr.boyaca.gov.co/wp-json/wp/v2/media/' + idJsonImagen).read())
imagen2 = leerImagen['media_details']['sizes']['medium']['source_url']

def mi_funcion():
	print (" ")
	print ("Cantidad de resultados:  " + cantidadResultados)
	print ("Encontré estos resultados:")
	for x in range(0,len(leer)):
		print (leer[x]['title']['rendered'])

mi_funcion()

print (" ")
print ("Título del atractivo:    " + leer[0]['title']['rendered'])
print ("Url del atractivo:       " + leer[0]['link'])
print ("Ciudad del atractivo:    " + leer[0]['ciudad'])
print ("Slug   del atractivo:    " + leer[0]['slug'])
print ("Id Imagen:               " + idJsonImagen)
print ("Imagen del atractivo 2:  " + imagen2)
print ("Excerpt del atractivo:   " + descripcion)
print (" ")
