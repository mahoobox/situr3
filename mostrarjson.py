from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json

def listadoBusqueda(dato_recuperado):
#	print (" ")
#	print ("Cantidad de resultados:  " + cantidadResultados)
	print (inicioFBCard)
#	print ("Encontré estos resultados:")
	for x in range(0,len(dato_recuperado)):
		descFichaAtrFB = re.sub("<.*?>", "", dato_recuperado[x]['excerpt']['rendered'])
		idImgFichaAtrFB = str(dato_recuperado[x]['featured_media'])
		print ("""                            {   
                                "title" : """ + dato_recuperado[x]['title']['rendered'] + """,
                                "image_url" : """ + idImgFichaAtrFB + """,
                                "subtitle": " Soy la descripción, colocar variable descFichaAtrFB ",
                                "buttons":  [
                                    {
                                        "type":"web_url",
                                        "url": """+dato_recuperado[x]['link']+""",
                                        "title": "Ver en SITUR"
                                    },
                                    {
                                        "type":"web_url",
                                        "url": """+dato_recuperado[x]['link']+""",
                                        "title": "boton2"
                                    }
                                ]
                            },""")



#		print (dato_recuperado[x]['title']['rendered'], end="")
	print (finFBCard)
	return

"""def listadoBusqueda(dato_recuperado):
    for x in range(0,len(dato_recuperado)):
        print (dato_recuperado[x]['title']['rendered'], end=", ")
    return

"""
inicioFBCard = """{
            "facebook" : {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type" : "generic",
                        "elements" : ["""

finFBCard = """]
                   }
                }
            }
        }"""

buscasitur = str(input("Ingrese el atractivo que desea buscar:   "))
#buscasitur = "laguna de tota"
buscasitur_sin_espacio = buscasitur.replace(" ", "%20")
print (buscasitur_sin_espacio)

leer = json.loads(urlopen('http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?orderby=relevance&search=' + buscasitur_sin_espacio).read())
cantidadResultados = str(len(leer))#Contar Cantidad de Resultados Encontrados
range(0,len(leer))#Rango que recorre la cantidad de resultados mostrados

test = leer[0].get('link')
test2 = leer[0]['title']['rendered']#Esta muestra el título 
descripcion = re.sub("<.*?>", "", leer[0]['excerpt']['rendered'])
tituloAtractivo = leer[0]['title']['rendered']
descripcionAtractivo = descripcion

#idJsonImagen = str(2739)
idJsonImagen = str(leer[0]['featured_media'])
leerImagen = json.loads(urlopen('http://www.situr.boyaca.gov.co/wp-json/wp/v2/media/' + idJsonImagen).read())
imagen2 = leerImagen['media_details']['sizes']['medium']['source_url']
imagenAtractivo = imagen2

print (" ")
print  (listadoBusqueda(leer), "HOLA MUNDO")
print (" ")
print (" ")
print ("Título del atractivo:    " + leer[0]['title']['rendered'])
print ("Url del atractivo:       " + leer[0]['link'])
print ("Ciudad del atractivo:    " + leer[0]['ciudad'])
print ("Slug   del atractivo:    " + leer[0]['slug'])
print ("Id Imagen:               " + idJsonImagen)
print ("Imagen del atractivo 2:  " + imagen2)
print ("Excerpt del atractivo:   " + descripcion)
print (" ")




"""        "data" : {  
                "facebook":{  
                    "text":"soy un texto, y si funciono"
                },
                "facebook" : {
                    "attachment" : {
                        "type" : "template",
                        "payload" : {
                            "template_type" : "generic",
                            "elements" : [
                                {
                                    "title" : tituloAtractivo,
                                    "image_url" : imagenAtractivo,
                                    "subtitle": descripcionAtractivo,
                                    "buttons":  [
                                        {
                                            "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver"
                                        },
                                        {
                                             "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver2"
                                        },
                                        {
                                              "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver3"
                                        }
                                    ]
                                },
                                {
                                    "title": tituloAtractivo,
                                    "image_url": imagenAtractivo,
                                    "subtitle": descripcionAtractivo,
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://www.moovrika.com/m/4167",
                                        "webview_height_ratio": "tall"
                                    },
                                    "buttons": [
                                        {
                                            "title": "more info",
                                            "type": "web_url",
                                            "url": "https://www.moovrika.com/m/4082",
                                            "webview_height_ratio": "tall"
                                        },
                                        {
                                             "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver2"
                                        },
                                        {
                                              "type":"web_url",
                                            "url": "http://situr.boyaca.gov.co",
                                            "title": "Ver3"
                                        }
                                    ]
                                }
                           ]
                       }
                    }
                }
            },"""