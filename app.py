#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import random
import MySQLdb
import sys

import re #retira etiquetas HTML de la descripción

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

soyversion = sys.version


def maindb(sqlcons):
  # Connect to the MySQL database
    db = MySQLdb.connect(host = '192.95.22.65', user = 'sitursit_bot', passwd = 'RwfMXSUurWCX', db = 'sitursit_bot')
    cursor = db.cursor()

 #   sql2 = """INSERT INTO `atractivos_cons` (`ID`, `fecha_hora`, `sexo`, `edad`, `ubicacion`, `atractivo_buscado`) VALUES (NULL, NULL, 'M', '28', 'Líbano, Colombia', 'casa terratota')"""

    cursor.execute(sqlcons)

    db.close()


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

def makeWebhookResult(req):
    accionEntrante=req.get("result").get("action")
    if accionEntrante == "buscarAtractivos":
        result = req.get("result")#invocar el result del busjson
        parameters = result.get("parameters")#invocar el parameters dentro de result
        atractivos = parameters.get("atractivos")#DATO TRAÍDO DE API.AI - ATRACTIVOS

        sql = """INSERT INTO `atractivos_cons` (`ID`, `fecha_hora`, `sexo`, `edad`, `ubicacion`, `atractivo_buscado`) VALUES (NULL, NULL, NULL, NULL, NULL, '"""+atractivos+"""')"""
        maindb(sql)

        cadenaConsulta = atractivos

        #URL BASE CONSULTA ATRACTIVOS JSON
        baseUrl = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?per_page=10&orderby=relevance&search="#URL Base Atractivos

        speech = " atractivos turísticos"

    elif accionEntrante == "buscarCiudad":
        result = req.get("result")#invocar el result del busjson
        parameters = result.get("parameters")#invocar el parameters dentro de result
        municipios = parameters.get("municipios")#DATO TRAÍDO DE API.AI - ATRACTIVOS

        sql = """INSERT INTO `ciudades_cons` (`ID`, `fecha_hora`, `sexo`, `edad`, `ubicacion`, `ciudad_buscada`) VALUES (NULL, NULL, NULL, NULL, NULL, '"""+municipios+"""')"""
        maindb(sql)

        cadenaConsulta = ""

        #URL BASE CONSULTA ATRACTIVOS JSON
        baseUrl = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?tags="+municipios+"&per_page=10"#URL Base Atractivos

        speech = " atractivos turísticos en la ciudad"

    elif accionEntrante == "buscarAtractivoCiudad":
        maindb()
        result = req.get("result")#invocar el result del busjson
        parameters = result.get("parameters")#invocar el parameters dentro de result
        atractivos = parameters.get("atractivos")#DATO TRAÍDO DE API.AI - ATRACTIVOS
        municipios = parameters.get("municipios")#DATO TRAÍDO DE API.AI - ATRACTIVOS

        sql = """INSERT INTO `atractivo_ciudad_cons` (`ID`, `fecha_hora`, `sexo`, `edad`, `ubicacion`, `atractivo_buscado`, `ciudad_buscada`) VALUES (NULL, NULL, NULL, NULL, NULL, 'parquecitos bot','25')"""
        maindb(sql)

        cadenaConsulta = atractivos + " " + municipios

        #URL BASE CONSULTA ATRACTIVOS JSON
        baseUrl = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?tags="+municipios+"&per_page=10&orderby=relevance&search="#URL Base Atractivos

        speech = " resultados para este atractivo en la ciudad    Versión: " + soyversion + " - Consulta - "

    elif accionEntrante == "buscarPrestador":
        result = req.get("result")#invocar el result del busjson
        parameters = result.get("parameters")#invocar el parameters dentro de result
        categorias_prestadores = parameters.get("categorias_prestadores")#DATO TRAÍDO DE API.AI - ATRACTIVOS
        municipios = parameters.get("municipios")#DATO TRAÍDO DE API.AI - ATRACTIVOS

        cadenaConsulta = ""

        #URL BASE CONSULTA ATRACTIVOS JSON
        baseUrl = "http://situr.boyaca.gov.co/wp-json/wp/v2/pst?tags="+municipios+"&categories="+categorias_prestadores+"&per_page=10"#URL Base Atractivos

        speech = " prestadores de servicios en esta ciudad"



    listaMensajesBuscando = ["Dame un momento, estoy buscando entre mis archivos...🔍", "Buscando...🔍", "Revisaré entre mis archivos...🔍"]#Mensajes que indican que se está realizando la búsqueda
    msgsBuscando = random.choice(listaMensajesBuscando)#Seleccion aleatoria de un mensaje
    
    retirarEspacios = cadenaConsulta.replace(" ",  "%20")#Retirar Espacios Atractivos

    leerJsonSitur = json.loads(urlopen(baseUrl + retirarEspacios).read())#Leer JSON SITUR

    cantidadResultados = str(len(leerJsonSitur))#Contar Cantidad de Resultados Encontrados
    speechResultados = "Mira 😃, encontré " + cantidadResultados + speech

    ##### ACA DEBE TERMINARSE LA FUNCIÓN LOCAL

    print("Response:")
    print(speech)

    return {
        "speech": "",
        "messages": [
        {
        "type": 0,
        "platform": "facebook",
        "speech": msgsBuscando
#        "speech": "Dame un momento, estoy buscando entre mis archivos...🔍"
        },
        {
        "type": 0,
        "platform": "facebook",
        "speech": speechResultados
        },
        {
          "type": 4,
          "platform": "facebook",
          "payload": listadoBusqueda(leerJsonSitur)
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
#        "data" :listadoBusqueda(leerJsonSitur),
#        "data" :fbMsg2,
#        "contextOut": [],
        "contextOut": [{"name":"desdepython", "lifespan":2}],
        "source": "soy-un-dato-irrelevante"
#        "source": listadoBusqueda(leerJsonSitur)
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
#        "data" :listadoBusqueda(leerJsonSitur),
#        "data" :fbMsg2,
#        "contextOut": [],
        "contextOut": [{"name":"desdepython", "lifespan":2}],
        "source": "soy-un-dato-irrelevante"
#        "source": listadoBusqueda(leerJsonSitur)
    }"""

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
