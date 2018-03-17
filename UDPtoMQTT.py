import socket
import json
import paho.mqtt.client as mqtt
from datetime import datetime

UDP_PORT_NO = 1902
MQTT_BROKER = "192.168.20.17"
MQTT_TOPIC = "/openhab/in/rfswitches/test"


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def printlog(message):
    print now() + " " + message


def on_connect(client, userdata, flags, rc):
    printlog("Connected to MQTT Broker with result code " + str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind(('', UDP_PORT_NO))

printlog("Listening on Port " + str(UDP_PORT_NO))

while True:
    data, addr = serverSock.recvfrom(1024)
    printlog("Received Message: " + data)
    temp = data.split('}')[1] + '}'
    # print "Temp: ", temp
    msg = json.loads(temp)
    # print "Data:", msg['data']
    # print "Type:", msg['type']
    client.publish(MQTT_TOPIC, msg['data'])
    printlog("Publish to " + MQTT_TOPIC + ", " + msg['data'])

