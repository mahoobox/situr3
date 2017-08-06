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
    pruebatitulos = ""
    varComa = 0
    for x in range(0,len(urlBaseJson)):
        tituloItem = urlBaseJson[x]['title']['rendered']
        descripcionItem = re.sub("<.*?>", "", urlBaseJson[x]['excerpt']['rendered'])#Descripción del atractivo eliminando etiquetas
#        idImgFichaAtrFB = str(urlBaseJson[x]['featured_media'])#ID de la imagen del atractivo
#        leerImagenAtractivos = json.loads(urlopen(urlBaseImagen + idImgFichaAtrFB).read())#Une la URL base de las imágenes con el ID de imagen y lo lee como JSON
#        imagenDefAtractivos = leerImagenAtractivos['media_details']['sizes']['medium']['source_url']#Interpreta el JSON de la imagen y extrae la URL de la imagen
        if varComa < len(urlBaseJson)-1:
            varComa = varComa +1
            print (varComa)
            comaJson = ","
        else:
            comaJson = ""
        pruebatitulos = pruebatitulos + ("""                            {
                                "title" : \"""" + tituloItem + """\",
                                "image_url" : "https://www.dondevive.org/wp-content/uploads/2015/08/donde-viven-los-conejos.jpg",
                                "subtitle": "Solo muestro 80 caracteres y 2 punticos... Este tiene 90 El esquí náutico se realiza en la",
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
                            }""" + str(comaJson) + """""")

    resultadoMauricio = inicioFBCard2+pruebatitulos+finFBCard2
#    resultadoMauricio = json.dumps(resultadoMauricio)
    resultadoMauricio = json.loads(resultadoMauricio)
    return resultadoMauricio

inicioFBCard = """{
            "facebook" : {
                "attachment" : {
                    "type" : "template",
                    "payload" : {
                        "template_type" : "generic",
                        "elements" : ["""

inicioFBCard2 = '{"facebook" : {"attachment" : {"type" : "template","payload" : {"template_type" : "generic","elements" : ['

finFBCard = """                        ]
                    }
                }
            }
        }"""

finFBCard2 = ']}}}}'

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

    speech = "Ye encontrado " + cantidadResultados + " Resultados .   El atractivo que solicitaste es: " + tituloAtractivo + "  y la url de la imagen es: " + imagenAtractivo

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data" :listadoBusqueda(leerAtractivo, baseUrlImgAtract),
#        "data" :finJsonBusqueda(),
#        "contextOut": [],
        "contextOut": [{"name":"desdepython", "lifespan":2}],
        "source": "soy-un-dato-irrelevante"
#        "source": listadoBusqueda(leerAtractivo)
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
