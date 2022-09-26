import googlemaps
from datetime import datetime
from main_gps import coordenadas

data_coordenadas = coordenadas
latitud = data_coordenadas['lat']
longitud = data_coordenadas['lon']
gmaps = googlemaps.Client(key='Add Your Key here')

# Geocoding an address
geocode_result = gmaps.geocode('Localizacion, MiDispositivoGPS')

# Look up an address with reverse geocoding


reverse_geocode_result = gmaps.reverse_geocode((latitud, longitud))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("GPS", "Lugar, Pais", mode="transit", departure_time=now)