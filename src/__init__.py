from Config import Config
from Sensor import Sensor
from Plot import Plot
from SensorList import SensorList
from Coordinates import Coordinates
from Historian import Historian

import paho.mqtt.client as mqtt

sensors = {}

config = Config('config.json')
plot = Plot(config)
sensorList = SensorList(config)
coordinates = Coordinates(config)
historian = Historian(config)


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(config.getMqttTopic())

def on_message(client, userdata, message):
    # Get a sensor from the message and put it in a list
    sensorList.addSensorFromMessage(message.payload)

    # Remove duplicates
    coordinatesToPlot = coordinates.objectListToSeperateList(
        coordinates.removeDuplicates(
            sensorList.getSensors()
        )
    )

    # Draw the image
    plot.draw(coordinatesToPlot)

    # Write to the historian
    plotX = coordinatesToPlot['x']
    plotY = coordinatesToPlot['y']
    for x, y in zip(plotX, plotY):
        historian.writeCoordinatesToFile(x, y)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(
    config.getMqttIp(),
    config.getMqttPort()
)

client.loop_forever()