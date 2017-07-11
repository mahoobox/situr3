from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json

#buscasitur = str(input("Ingrese el atractivo que desea buscar:   "))
buscasitur = "2890"
buscasitur_sin_espacio = buscasitur.replace(" ", "%20")
print (buscasitur_sin_espacio)

leer = json.loads(urlopen('http://www.situr.boyaca.gov.co/wp-json/wp/v2/media/' + buscasitur_sin_espacio).read())


print (" ")
#print (leer)
print (leer['guid']['rendered'])
print (leer['media_details']['sizes']['full']['source_url'])
print (" ")
