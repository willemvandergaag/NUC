from Config import Config
from Plot import Plot
from SensorList import SensorList
from Coordinates import Coordinates
from Historian import Historian
from Heatmap import Heatmap

import paho.mqtt.client as mqtt

sensors = {}
# config file
config = Config('config.json')
plot = Plot(config.getRoomX(),
            config.getRoomY(),
            config.getSensorLocations(),
            config.getImage('room'),
            config.getTempLimit(),
            config.getOpeningTime(),
            config.getClosingTime(),
            config.getSocialDistancing())
sensorList = SensorList(config.getSensorXOffset(),
                        config.getSensorYOffset(),
                        config.getXMultiplier(),
                        config.getYMultiplier(),
                        config.getSensorLocations())
coordinates = Coordinates(config.getMaxDifference())
historian = Historian(config.getHistorianFolder(),
                      config.getHistorianFilePrefix(),
                      config.getHistorianHeaders())
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
        allSensors = sensorList.addSensorFromMessage(message.payload)
    except:
        return

    coordinatesWithoutDuplicates = coordinates.removeDuplicates(
        allSensors
    )

    # Remove duplicates
    coordinatesToPlot = coordinates.objectListToSeperateList(
        coordinatesWithoutDuplicates
    )

    # Draw the image
    plot.draw(coordinatesToPlot, allSensors)

    # Display heatmap
    heatmap.createHeatmap(coordinatesToPlot)

    try:
        # Write to the historian
        for sensor in coordinatesWithoutDuplicates:
            plotX = sensor['x']
            plotY = sensor['y']
            id = sensor['id']
            historian.writeCoordinatesToFile(id, plotX, plotY)
    except:
        pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect to broker
client.connect(
    config.getMqttIp(),
    config.getMqttPort()
)


client.loop_forever()
