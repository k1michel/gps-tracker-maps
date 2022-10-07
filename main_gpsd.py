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
    if packet.mode >=2:
        lat,lon = packet.position()
        fecha = packet.time
        fecha_compuesta = fecha.split('T')
        fecha_ok = fecha_compuesta[0]
        hora_ok = fecha_compuesta[1]    

        url_map = str(packet.map_url())
        envio= dict(
            n_satelites = str(packet.sats),
            fecha = fecha_ok,
            hora = hora_ok,
            velocidad_h = packet.hspeed,
            velocidad_v = packet.speed(),
            latitud = lat,
            longitud = lon,
            altitud = packet.alt,
            url = url_map,

        )
        return envio


if __name__ == '__main__':
    uvicorn.run(api_gpsd, host="0.0.0.0", port=8000)