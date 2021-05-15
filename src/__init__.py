from Config import Config
from Plot import Plot
from SensorList import SensorList
from Coordinates import Coordinates
from Historian import Historian
from Heatmap import Heatmap

import paho.mqtt.client as mqtt

sensors = {}

config = Config('config.json')
plot = Plot(config.getRoomX(),
            config.getRoomY(),
            config.getSensorLocations(),
            config.getImage('room'),
            config.getTempLimit())
sensorList = SensorList(config.getSensorXOffset(),
                        config.getSensorYOffset(),
                        config.getXMultiplier(),
                        config.getYMultiplier(),
                        config.getSensorLocations())
coordinates = Coordinates(config.getMaxDifference())
historian = Historian(config.getHistorianFolder(),
                      config.getHistorianFilePrefix())
heatmap = Heatmap(config.getAverageHeatmapTemp(),
                  config.getRoomX(),
                  config.getRoomY(),
                  config.getXMultiplier(),
                  config.getYMultiplier())


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(config.getMqttTopic())


def on_message(client, userdata, message):
    try:
        # Get a sensor from the message and put it in a list
        sensorList.addSensorFromMessage(message.payload)
    except:
        return

    # Remove duplicates
    coordinatesToPlot = coordinates.objectListToSeperateList(
        coordinates.removeDuplicates(
            sensorList.getSensors()
        )
    )

    # Draw the image
    plot.draw(coordinatesToPlot, sensorList.getSensors())

    # Display heatmap
    heatmap.createHeatmap(coordinatesToPlot)

    try:
        # Write to the historian
        plotX = coordinatesToPlot['x']
        plotY = coordinatesToPlot['y']
        for x, y in zip(plotX, plotY):
            historian.writeCoordinatesToFile(x, y)
    except:
        pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(
    config.getMqttIp(),
    config.getMqttPort()
)

client.loop_forever()