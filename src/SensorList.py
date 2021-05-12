import json
from Sensor import Sensor

class SensorList:
    def __init__(self, config):
        self.__config = config
        self.__sensors = {}
    
    def __getTempAlert(self):
        return self.data['tempAlert']

    def __getClusters(self):
        return self.data['clusters']

    def __getHumans(self):
        return self.data['humans']
    
    def __getId(self):
        return self.data['sensor']

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
        sensor = Sensor(self.__config)

        sensor.setId(self.__getId())

        sensor.setTempAlert(
            self.__getTempAlert() > 0 if True else False
        )

        sensor.setHumans(self.__getHumans())
        sensor.setHeatmaps(self.__getHeatmaps())

        sensor.setOffsetX(self.__config.getSensorXOffset())
        sensor.setOffsetY(self.__config.getSensorYOffset())

        self.__populateX(sensor)
        self.__populateY(sensor)
        
        return sensor

    def __appendToSensors(self, sensor):
        self.__sensors[sensor.getId()] = sensor

    def getSensors(self):
        return self.__sensors

    def addSensorFromMessage(self, message):
        messageJSON = json.loads(message)
        self.data = messageJSON['data']
        self.__appendToSensors(
            self.__getSensorFromMessage()
        )
