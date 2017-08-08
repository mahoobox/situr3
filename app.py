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

    speech = "Hola, encontre estos resultdos: " + cantidadResultados

    print("Response:")
    print(speech)

    return {
        "speech": "",
        "messages": [
        {
        "type": 0,
        "speech": "Dame un momento, estoy buscando entre mis archivos..."
        },
        {
        "type": 3,
        "imageUrl": "http://www.situr.boyaca.gov.co/wp-content/uploads/2017/05/Plaza-de-Toros-Cesar-Rincón-Andres-Socadagüi-300x238.jpg"
        }
        ],
#        "speech": speech,
#        "displayText": speech,
#        "data" :listadoBusqueda(leerAtractivo),
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
