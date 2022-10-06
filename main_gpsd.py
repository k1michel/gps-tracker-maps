import gpsd
from datetime import datetime
import requests
import json
import webbrowser
from typing import Optional   
from fastapi import FastAPI, Request
from pydantic import BaseModel  
import uvicorn

## CREACION API ##
api_gpsd = FastAPI() 


## PETICIONES ##
@api_gpsd.get("/url")
def get_envios():  
    #Conectar con localhost de gpsd
    gpsd.connect(host='localhost')


    #Obtener datos del gps
    packet = gpsd.get_current()

    #Datos de respuesta del gps
    print(" ************ DATOS DEL GPS ************* ")
    print("  MODO: " + str(packet.mode))
    print("SATELITES: " + str(packet.sats))
    if packet.mode >= 2:
        print("  LATITUD: " + str(packet.lat))
        print(" LONGITUD: " + str(packet.lon))
        print(" TRACK: " + str(packet.track))
        print("  VELOCIDAD HORIZONTAL: " + str(packet.hspeed))
        print(" FECHA: " + str(packet.time))
        print(" ERROR: " + str(packet.error))
    else:
        print("  LATITUD: SIN DATOS")
        print(" LONGITUD: SIN DATOS")
        print(" TRACK: SIN DATOS")
        print("  VELOCIDAD HORIZONTAL: SIN DATOS")
        print(" ERROR: SIN DATOS")

    if packet.mode >= 3:
        print("  ALTITUD: " + str(packet.alt))
        print(" ELEVACION: " + str(packet.climb))
    else:
        print("  ALTITUD: SIN DATOS")
        print(" ELEVACION: SIN DATOS")

    print(" ************** DATOS COMPLEJOS DEL GPS ************** ")
    if packet.mode >= 2:
        print("  LOCALIZACION: " + str(packet.position()))
        print(" VELOCIDAD: " + str(packet.speed()))
        print("PRECISION DE POSICION: " + str(packet.position_precision()))
        print("   MAPA URL: " + str(packet.map_url()))
    else:
        print("  LOCALIZACION: SIN DATOS")
        print(" VELOCIDAD: SIN DATOS")
        print(" PRECISION DE POSICION: SIN DATOS")
        print("   MAPA URL: SIN DATOS")

    if packet.mode >= 3:
        print("  ALTITUD: " + str(packet.altitude()))
    else:
        print("  ALTITUD: SIN DATOS")


    print(" ************* FUNCIONES DEL GPS ************* ")
    print("DISPOSITIVO: " + str(gpsd.device()))

    print('\n ##########  MIS DATOS  #########')
    lat,lon = packet.position()
    print(f'Latitud: {lat} \nLongitud: {lon}')

    url_map = str(packet.map_url())
    envio= dict(
        latitud = lat,
        longitud = lon,
        url = url_map,

    )
    return envio
#webbrowser.open(url_map)



### TOM TOM ###
'''
#locations = str(round(lat,5)) + ',' + str(round(lon,5)) + ':' + str(round(lat+10,5)) + ',' + str(round(lon+10,5))
#post_tomtom=requests.get(f'https://api.tomtom.com/routing/1/calculateRoute/{locations}/json?key=0RIbAqPHzVq7IyARS5U9Uig03lOGtRoS')
post_tomtom=requests.get(f'https://api.tomtom.com/map/1/staticimage?key=0RIbAqPHzVq7IyARS5U9Uig03lOGtRoS&zoom=15&center={lon},{lat}&format=png&layer=basic&style=main&width=300&height=200&view=Unified&language=es-ES').content
with open(f'mapa_{packet.time}.png','wb') as down_img:
    down_img.write(post_tomtom)
'''

### GOOGLE MAPS ###
'''
gmaps = googlemaps.Client(key='-')

# Geocoding an address
geocode_result = gmaps.geocode('Localizacion, MiDispositivoGPS')

# Look up an address with reverse geocoding


reverse_geocode_result = gmaps.reverse_geocode((lat, lon))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("GPS", "Lugar, Pais", mode="transit", departure_time=now)
'''

if __name__ == '__main__':
    uvicorn.run(api_gpsd, host="0.0.0.0", port=8000)