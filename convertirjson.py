from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json

#leerAtractivo = json.loads(urlopen(baseUrlAtractivos + retirarEspacios).read())

archivo = json.loads(open("jsontest.json").read())
print (archivo)
print (" ")
variable = 0
limiteConsulta = 5
for x in range(0,limiteConsulta):
	print ("hola mundo")
	if variable < limiteConsulta - 1:
		variable = variable +1
		print (variable)
	else :
		print ("")




#print (repr(archivo))
#archivo.write(str((resultadoMauricio)))
#archivo.close
