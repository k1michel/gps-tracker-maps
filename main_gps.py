from time import sleep
import serial
import sys

while True:
    with serial.Serial() as ser:
        ser.baudrate = 9600
        ser.port = '/dev/ttyUSB0'
        ser.open()
        gps_serial = ser.read()

    def coordenadas(latitud, longitud):
        lat_recibed = latitud
        lon_recibed = longitud

        lat_deg = latitud[0:2]   
        lat_mins = latitud[2:4]  
        lat_secs = round(float(latitud[5:])*60/10000, 2)
    
        lat_str = lat_deg +  '['+ lat_mins + '(' + str(lat_secs) + ')'

        lon_deg = longitud[0:3] 
        lon_mins = longitud[3:5]
        lon_secs = round(float(longitud[6:])*60/10000, 2)
    
        lon_str = lon_deg +  "["+ lon_mins + "(" + str(lon_secs) + ')'

        data = dict(
            lat = lat_recibed,
            lon = lon_recibed,
        )
        print(data)
        return gps_serial
    #ejecutar = coordenadas()
    print(gps_serial)
    sleep(2)

