from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import re

import json

def listadoBusqueda(urlBaseJson, urlBaseImagen):
	print (urlBaseImagen)
#	print ("Cantidad de resultados:  " + cantidadResultados)
#	print (inicioFBCard)
#	print ("Encontré estos resultados:")
	pruebatitulos2 = ""
	for x in range(0,len(urlBaseJson)):
		tituloItem = urlBaseJson[x]['title']['rendered']
		descripcionItem = re.sub("<.*?>", "", urlBaseJson[x]['excerpt']['rendered'])#Descripción del atractivo eliminando etiquetas
		idImgFichaAtrFB = str(urlBaseJson[x]['featured_media'])#ID de la imagen del atractivo
		leerImagenAtractivos = json.loads(urlopen(urlBaseImagen + idImgFichaAtrFB).read())#Une la URL base de las imágenes con el ID de imagen y lo lee como JSON
		imagenDefAtractivos = leerImagenAtractivos['media_details']['sizes']['medium']['source_url']#Interpreta el JSON de la imagen y extrae l-a URL de la imagen
		
		pruebatitulos2 = pruebatitulos2 + ("""                            {   
                                "title" : \"""" + tituloItem + """\",
                                "image_url" : \""""+ imagenDefAtractivos +"""\",
                                "subtitle": "Soy la descripción, colocar variable descripcionItem",
                                "buttons":  [
                                    {
                                        "type":"web_url",
                                        "url": \""""+urlBaseJson[x]['link']+"""\",
                                        "title": "Ver en SITUR"
                                    },
                                    {
                                        "type":"web_url",
                                        "url": \""""+urlBaseJson[x]['link']+"""\",
                                        "title": "boton2"
                                    }
                                ]
                            },""")

#	print (pruebatitulos)
#	print (pruebatitulos2)
	resultadoMauricio = inicioFBCard+pruebatitulos2+finFBCard
	return resultadoMauricio

inicioFBCard = """\"\"\"{
            "facebook" : {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type" : "generic",
                        "elements" : ["""

inicioFBCard2 = """{"facebook" : {"attachment" : {"type" : "template","payload" : {"template_type" : "generic","elements" : ["""

finFBCard = """                        ]
                    }
                }
            }
        }\"\"\""""

finFBCard2 = """]}}}}"""

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
baseUrlImgAtract = "http://www.situr.boyaca.gov.co/wp-json/wp/v2/media/"#URL Base Imagenes Atractivos
imagen2 = leerImagen['media_details']['sizes']['medium']['source_url']
imagenAtractivo = imagen2

print (" ")
print  (listadoBusqueda(leer, baseUrlImgAtract))
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
            },


fbMsg2 = {
        "facebook" : {
            "attachment" : {
                "type" : "template",
                "payload" : {
                    "template_type" : "generic",
                    "elements" : [
                        {   
                            "title" : "soy el titulo tst2 conj",
                            "image_url" : "https://www.anipedia.net/imagenes/taxonomia-conejos.jpg",
                            "subtitle": "soy la descripcion",
                            "buttons":  [
                                {
                                    "type":"web_url",
                                    "url": "http://situr.boyaca.gov.co",
                                    "title": "boton1"
                                },
                                {
                                    "type":"web_url",
                                    "url": "http://situr.boyaca.gov.co",
                                    "title": "boton2"
                                },
                                {
                                    "type":"web_url",
                                    "url": "http://situr.boyaca.gov.co",
                                    "title": "boton3"
                                }
                            ]
                        },
                        {
                            "title": "soy el otro titulo",
                            "image_url": "https://www.dondevive.org/wp-content/uploads/2015/08/donde-viven-los-conejos.jpg",
                            "subtitle": "soy la descripción",
                            "default_action": {
                                "type": "web_url",
                                "url": "https://www.moovrika.com/m/4167",
                                "webview_height_ratio": "tall"
                            },
                            "buttons": [
                                {
                                    "title": "más info",
                                    "type": "web_url",
                                    "url": "https://www.moovrika.com/m/4082",
                                    "webview_height_ratio": "tall"
                                },
                                {
                                    "type":"web_url",
                                    "url": "http://situr.boyaca.gov.co",
                                    "title": "boton2"
                                },
                                {
                                    "type":"web_url",
                                    "url": "http://situr.boyaca.gov.co",
                                    "title": "boton3"
                                }
                            ]
                        },
                    ]
                }
            }
        }
    }

    fbMsg = {
            "facebook" : {
#                "text":{
#                    "Hola Mundo, si funciono"
#                },
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
                                        "title": "boton1"
                                    },
                                    {
                                         "type":"web_url",
                                        "url": "http://situr.boyaca.gov.co",
                                        "title": "boton2"
                                    },
                                    {
                                          "type":"web_url",
                                        "url": "http://situr.boyaca.gov.co",
                                        "title": "boton3"
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
                                        "title": "más info",
                                        "type": "web_url",
                                        "url": "https://www.moovrika.com/m/4082",
                                        "webview_height_ratio": "tall"
                                    },
                                    {
                                         "type":"web_url",
                                        "url": "http://situr.boyaca.gov.co",
                                        "title": "boton2"
                                    },
                                    {
                                          "type":"web_url",
                                        "url": "http://situr.boyaca.gov.co",
                                        "title": "boton3"
                                    }
                                ]
                            }
                       ]
                   }
                }
            }
        }



    """