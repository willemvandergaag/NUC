from Config import Config
from Sensor import Sensor
from Plot import Plot
from SensorList import SensorList
from Coordinates import Coordinates

import paho.mqtt.client as mqtt

sensors = {}

config = Config('config.json')
plot = Plot(config)
sensorList = SensorList(config)
coordinates = Coordinates(config)

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(config.getMqttTopic())

def on_message(client, userdata, message):
    # Get a sensor from the message and put it in a list
    sensorList.addSensorFromMessage(message.payload)

    # Remove duplicates
    coordinatesToPlot = coordinates.removeDuplicates(
        sensorList.getSensors()
    )

    # plot.show(coordinatesToPlot)
    plot.blit(coordinatesToPlot)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(
    config.getMqttIp(),
    config.getMqttPort()
)

client.loop_forever()