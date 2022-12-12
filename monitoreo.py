import pyaudio
import wave
import os
import time
import sys
import board
import paho.mqtt.client as mqtt
from datetime import datetime
import json
from array import array

FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100
CHUNK=100024
RECORD_SECONDS=15

THINGSBOARD_HOST = 'iot.ceisufro.cl'
ACCESS_TOKEN = '####'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'estado': False,'ruido':0, 'fecha':'date'}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
#client.connect(THINGSBOARD_HOST, 8080, 60)
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

audio=pyaudio.PyAudio() #instantiate the pyaudio

        #recording prerequisites
stream=audio.open(format=FORMAT,channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)
frames=[]

SERVER = 'smtp-mail.outlook.com'
FROM = "proyectomonitordci@outlook.com"
TO = ["proyectomonitordci@yopmail.com"]

SUBJECT = "Alerta!"
TEXT = "Se registra un ruido muy fuerte\n Revisar: http://localhost:8081/"

message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail
import smtplib
try:
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
except Exception as e:
    print(e)
    server = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
server.ehlo()
server.starttls()
server.login("proyectomonitordci@outlook.com", "PASSWORD")


while True:
    for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
       
        data=stream.read(CHUNK)
        data_chunk=array('h',data)
        vol=max(data_chunk)
        if(vol>=16000):
            estado = True
            ruido=vol
            print("Se registra ruido")
            sensor_data['estado'] = estado
            sensor_data['ruido'] = vol
            fecha = datetime.now()
            fecha = fecha.strftime("%b %d %Y %H:%M:%S")
            sensor_data['fecha'] = fecha
            print(u"Estado: {:g}, Ruido: {:g}, Fecha: ".format(estado,ruido))
            print(fecha)
            print(message)
            server.sendmail(FROM, TO, message)
           
            frames.append(data)
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
            next_reading += INTERVAL
            sleep_time = next_reading-time.time()
            if sleep_time > 0:
                   
                    time.sleep(sleep_time)
        else:
            estado=False
            print("nothing")
        print("\n")


client.loop_stop()
client.disconnect()
