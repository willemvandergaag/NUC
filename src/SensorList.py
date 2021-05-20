import json
from Sensor import Sensor


class SensorList:
    def __init__(self, sensorXOffset, sensorYOffset, xMultiplier, yMultiplier, sensorLocations):
        self.__sensorXOffset = sensorXOffset
        self.__sensorYOffset = sensorYOffset
        self.__xMultiplier = xMultiplier
        self.__yMultiplier = yMultiplier
        self.__sensorLocations = sensorLocations
        self.__sensors = {}

    def __getTempAlert(self):
        return self.__data['tempAlert']

    def __getClusters(self):
        return self.__data['clusters']

    def __getHumans(self):
        return self.__data['humans']

    def __getId(self):
        return self.__data['sensor']

    def __getHeatmaps(self):
        heatmapsTemp = []
        for cluster in self.__getClusters():
            heatmapsTemp.append(cluster['heatmaps'])

        return heatmapsTemp

    def __populateX(self, sensor):
        for cluster in self.__getClusters():
            sensor.appendToX(cluster['coordinates']['x'])

    def __populateY(self, sensor):
        for cluster in self.__getClusters():
            sensor.appendToY(cluster['coordinates']['y'])

    def __appendToSensors(self, sensor):
        self.__sensors[sensor.getId()] = sensor

    def __getSensorFromMessage(self):
        # get all sensor values from a message
        sensor = Sensor(self.__xMultiplier, self.__yMultiplier,
                        self.__sensorLocations)

        sensor.setId(self.__getId())

        sensor.setTempAlert(self.__getTempAlert())

        sensor.setHumans(self.__getHumans())
        sensor.setHeatmaps(self.__getHeatmaps())

        sensor.setOffsetX(self.__sensorXOffset)
        sensor.setOffsetY(self.__sensorYOffset)

        self.__populateX(sensor)
        self.__populateY(sensor)

        return sensor

    def __appendToSensors(self, sensor):
        self.__sensors[sensor.getId()] = sensor

    def getSensors(self):
        return self.__sensors

    def addSensorFromMessage(self, message):
        messageJSON = json.loads(message)
        self.__data = messageJSON['data']
        self.__appendToSensors(
            self.__getSensorFromMessage()
        )
        return self.getSensors()
