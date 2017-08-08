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

def listadoBusqueda(urlBaseJson):
    pruebatitulos = ""
    varComa = 0
    for x in range(0,len(urlBaseJson)):
        tituloItem = urlBaseJson[x]['title']['rendered']
        imagenDefAtractivos = urlBaseJson[x]['better_featured_image']['media_details']['sizes']['medium']['source_url']
#        descripcionItem = re.sub("<.*?>", "", (urlBaseJson[x]['excerpt']['rendered'])[0:85])#Descripción del atractivo eliminando etiquetas
        if varComa < len(urlBaseJson)-1:
            varComa = varComa +1
            print (varComa)
            comaJson = ","
        else:
            comaJson = ""
        pruebatitulos = pruebatitulos + ("""                            {
                                "title" : \""""+tituloItem+"""\",
                                "image_url" : \""""+imagenDefAtractivos+"""\",
                                "subtitle": \""""+tituloItem+"""\",
                                "buttons":  [
                                    {
                                        "type":"web_url",
                                        "url": \""""+urlBaseJson[x]['link']+"""\",
                                        "title": "Ver en SITUR"
                                    }
                                ]
                            }""" + str(comaJson) + """""")

    resultadoMauricio = inicioFBCard+pruebatitulos+finFBCard
#    resultadoMauricio = json.dumps(resultadoMauricio)
    resultadoMauricio = json.loads(resultadoMauricio)
    return resultadoMauricio


inicioFBCard = '{"facebook" : {"attachment" : {"type" : "template","payload" : {"template_type" : "generic","elements" : ['

finFBCard = ']}}}}'


putafuncion = """{
            "facebook": {
              "attachment": {
                "type": "template",
                "payload": {
                  "template_type": "generic",
                  "elements": [
                    {
                      "title": "HE VUELTO y con más",
                      "image_url": "http://www.boyaca.gov.co/SecCultura/images/MARCA%20REGION%20BOYACA%20ES%20PARA%20VIVIRLA-1.jpg",
                      "subtitle": "soy la descripcion",
                      "buttons": [
                        {
                          "type": "web_url",
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
                          "type": "web_url",
                          "url": "http://situr.boyaca.gov.co",
                          "title": "boton3"
                        }
                      ]
                    }
                  ]
                }
              }
            }
          }"""

putafuncion = json.loads(putafuncion)

def makeWebhookResult(req):
    if req.get("result").get("action") != "buscarAtractivos":
        return {}
    result = req.get("result")#invocar el result del json 
    parameters = result.get("parameters")#invocar el parameters dentro de result
    atractivos = parameters.get("atractivos")#DATO TRAÍDO DE API.AI - ATRACTIVOS
    
    #URL BASE CONSULTA ATRACTIVOS JSON
    baseUrlAtractivos = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?per_page=10&orderby=relevance&search="#URL Base Atractivos
    retirarEspacios = atractivos.replace(" ",  "%20")#Retirar Espacios Atractivos

    leerAtractivo = json.loads(urlopen(baseUrlAtractivos + retirarEspacios).read())
    cantidadResultados = str(len(leerAtractivo))#Contar Cantidad de Resultados Encontrados

    speech = "Mira 😃, encontre " + cantidadResultados+ " resultados"

    print("Response:")
    print(speech)

    return {
        "speech": "",
        "messages": [
        {
        "type": 0,
        "platform": "facebook",
        "speech": "Dame un momento, estoy buscando entre mis archivos...🔍"
        },
        {
        "type": 0,
        "platform": "facebook",
        "speech": speech
        },
        {
          "type": 4,
          "platform": "facebook",
          "payload": listadoBusqueda(leerAtractivo)
        }
#        {
#          "type": 2,
#          "platform": "facebook",
#          "title": "Por favor escoge un elemento",
#          "replies": [
#            "Ver más"
#          ]
#        },
#        {
#          "type": 2,
#          "platform": "facebook",
#          "title": "Por favor escoge un elemento",
#         "replies": [
#            "Ver más"
#          ]
#        }
        ],
#        "speech": speech,
#        "displayText": speech,
#        "data" :listadoBusqueda(leerAtractivo),
#        "data" :fbMsg2,
#        "contextOut": [],
        "contextOut": [{"name":"desdepython", "lifespan":2}],
        "source": "soy-un-dato-irrelevante"
#        "source": listadoBusqueda(leerAtractivo)
    }

"""    return {
        "speech": "",
        "messages": [
        {
        "type": 0,
        "platform": "facebook",
        "speech": "Dame un momento, estoy buscando entre mis archivos..."
        },
        {
        "type": 0,
        "platform": "facebook",
        "speech": speech
        },
        {
          "type": 4,
          "platform": "facebook",
          "payload": {
            "facebook": {
              "attachment": {
                "type": "template",
                "payload": {
                  "template_type": "generic",
                  "elements": [
                    {
                      "title": "HE VUELTO y con más",
                      "image_url": "http://www.boyaca.gov.co/SecCultura/images/MARCA%20REGION%20BOYACA%20ES%20PARA%20VIVIRLA-1.jpg",
                      "subtitle": "soy la descripcion",
                      "buttons": [
                        {
                          "type": "web_url",
                          "url": "http://situr.boyaca.gov.co",
                          "title": "boton1"
                        },
                        {
                          "type": "web_url",
                          "url": "http://situr.boyaca.gov.co",
                          "title": "boton2"
                        },
                        {
                          "type": "web_url",
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
                          "type": "web_url",
                          "url": "http://situr.boyaca.gov.co",
                          "title": "boton2"
                        },
                        {
                          "type": "web_url",
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
        },
        {
          "type": 2,
          "platform": "facebook",
          "title": "Por favor escoge un elemento",
          "replies": [
            "blanco",
            "gris",
            "negro"
          ]
        }
        ],
#        "speech": speech,
#        "displayText": speech,
#        "data" :listadoBusqueda(leerAtractivo),
#        "data" :fbMsg2,
#        "contextOut": [],
        "contextOut": [{"name":"desdepython", "lifespan":2}],
        "source": "soy-un-dato-irrelevante"
#        "source": listadoBusqueda(leerAtractivo)
    }"""
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
