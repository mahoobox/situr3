#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

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

def makeWebhookResult(req):
    if req.get("result").get("action") != "buscarAtractivos":
        return {}
    result = req.get("result")#invocar el result del json 
    parameters = result.get("parameters")#invocar el parameters dentro de result
    atractivos = parameters.get("atractivos")#DATO TRAÍDO DE API.AI - ATRACTIVOS
    
    baseUrl = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?search="
    retirarEspacios = atractivos.replace(" ",  "%20")
    
    leer = json.loads(urlopen(baseUrl + retirarEspacios).read())
    nombre_atractivo = leer[0]['title']['rendered']
    descripcion_atractivo = leer[0]['excerpt']['rendered']
    url_atractivo = leer[0].get('link')

    cost = {'parque':100, 'casa':200, 'carro':300, 'reloj':400, 'Parque El Solano':500}#diccionario de datos

    speech = "El elemento que solicitaste es: " + atractivos + " y su valor asignado es  " + str(cost[atractivos]) + "          además estos datos del JSON: " + nombre_atractivo

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {
            "facebook" : {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                       {
                        "title":"b",
                        "image_url":"https://public.tableau.com/static/images/SI/SITURBoyacTurismoEmisor0_1/Inicio/1_rss.png",
                        "subtitle":"Weve got the right hat for everyone.",
                        "default_action": {
                          "type": "web_url",
                          "url": "https://peterssendreceiveapp.ngrok.io/view?item=103",
                          "messenger_extensions": true,
                          "webview_height_ratio": "tall",
                          "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                        },
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":"https://petersfancybrownhats.com",
                            "title":"View Website"
                          },{
                            "type":"postback",
                            "title":"Start Chatting",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                          }              
                        ]      
                      }
                    ]
                  }
                }
            }
        },
        "contextOut": [{"name":"desdepython", "lifespan":2, "parameters":{"slug":url_atractivo}}],
        "source": "apiai-situr3"
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
