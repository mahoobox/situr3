#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

import re #retira etiquetas HTML de la descripción

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)#Invoca función de consulta y muestra speech al situr3

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def listadoBusqueda(urlBaseJson, urlBaseImagen):
    def inicioFuncion():
        return inicioFBCard
    inicioFuncion()
    for x in range(0,len(urlBaseJson)):
#        descripcionItem = re.sub("<.*?>", "", urlBaseJson[x]['excerpt']['rendered'])#Descripción del atractivo eliminando etiquetas
#        idImgFichaAtrFB = str(urlBaseJson[x]['featured_media'])#ID de la imagen del atractivo
#        leerImagenAtractivos = json.loads(urlopen(urlBaseImagen + idImgFichaAtrFB).read())#Une la URL base de las imágenes con el ID de imagen y lo lee como JSON
#        imagenDefAtractivos = leerImagenAtractivos['media_details']['sizes']['medium']['source_url']#Interpreta el JSON de la imagen y extrae la URL de la imagen
        def dentroFuncion():
            return ("""                            {
                                "title" : "hola soy tu puto titulo",
                                "image_url" : "https://www.dondevive.org/wp-content/uploads/2015/08/donde-viven-los-conejos.jpg",
                                "subtitle": "Soy la descripción, colocar variable descripcionItem",
                                "buttons":  [
                                    {
                                        "type":"web_url",
                                        "url": "http://www.situr.boyaca.gov.co",
                                        "title": "Ver en SITUR"
                                    },
                                    {
                                        "type":"web_url",
                                        "url": "http://www.situr.boyaca.gov.co",
                                        "title": "boton2"
                                    }
                                ]
                            },""")
        dentroFuncion()
    return finFBCard

inicioFBCard = """{
            "facebook" : {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type" : "generic",
                        "elements" : ["""

finFBCard = """                        ]
                    }
                }
            }
        }"""

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

def mostrarFB():
    return fbMsg2

def makeWebhookResult(req):
    if req.get("result").get("action") != "buscarAtractivos":
        return {}
    result = req.get("result")#invocar el result del json 
    parameters = result.get("parameters")#invocar el parameters dentro de result
    atractivos = parameters.get("atractivos")#DATO TRAÍDO DE API.AI - ATRACTIVOS
    
    #URL BASE CONSULTA ATRACTIVOS JSON
    baseUrlAtractivos = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?orderby=relevance&search="#URL Base Atractivos
    baseUrlImgAtract = "http://www.situr.boyaca.gov.co/wp-json/wp/v2/media/"#URL Base Imagenes Atractivos
    retirarEspacios = atractivos.replace(" ",  "%20")#Retirar Espacios Atractivos

    leerAtractivo = json.loads(urlopen(baseUrlAtractivos + retirarEspacios).read())
    cantidadResultados = str(len(leerAtractivo))#Contar Cantidad de Resultados Encontrados
    range(0,len(leerAtractivo))#Rango que recorre la cantidad de resultados mostrados

    tituloAtractivo = leerAtractivo[0]['title']['rendered']
    descripcionAtractivo = re.sub("<.*?>", "", leerAtractivo[0]['excerpt']['rendered'])
    urlAtractivo = leerAtractivo[0].get('link')
    idImagenAtractivo = str(leerAtractivo[0]['featured_media'])

    leerImagenAtr = json.loads(urlopen(baseUrlImgAtract + idImagenAtractivo).read())
    imagenAtractivo = leerImagenAtr['media_details']['sizes']['medium']['source_url']

    speech = "We encontrado " + cantidadResultados + " Resultados .   El atractivo que solicitaste es: " + tituloAtractivo + "  y la url de la imagen es: " + imagenAtractivo
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

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data" :listadoBusqueda(leerAtractivo, baseUrlImgAtract),
#        "data" :mostrarFB(),
#        "contextOut": [],
        "contextOut": [{"name":"desdepython", "lifespan":2}],
        "source": "soy-un-dato-irrelevante"
#        "source": listadoBusqueda(leerAtractivo)
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
