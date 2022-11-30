#Original Code by Thingsboard Team
#Modified by Adesola Samuel
import os
import time
import sys
import board
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'iot.ceisufro.cl'
ACCESS_TOKEN = 'pZxD9DKkDKcwmpZtf9rY'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'estado_ruido': True}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
#client.connect(THINGSBOARD_HOST, 8080, 60)
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        estado = True
        print(estado)
        sensor_data['estado_ruido'] = estado

        # Sending  data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
