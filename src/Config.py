import json


class Config:
    def __init__(self, file):
        self.__config = {}

        self.__openFileToJSON(file)

    # Opens a configuration file
    # @return a JSON object
    def __openFileToJSON(self, file):
        self.__config = json.load(
            open(file)
        )

    def getRoomX(self):
        return self.__config['room']['width']

    def getRoomY(self):
        return self.__config['room']['length']

    def getNumberOfSensors(self):
        return self.__config['sensors']['number']

    def getMaxDifference(self):
        return self.__config['humans']['max_offset']

    def getSensorXOffset(self):
        return self.__config['sensors']['offset']['x']

    def getSensorYOffset(self):
        return self.__config['sensors']['offset']['y']

    def getSensorOffsets(self, sensorId):
        # Sensors have a name from 1 upwards, arrays are 0-indexed
        sensorId = sensorId - 1
        offsetX = self.__config['locations'][sensorId]['x'] - \
            self.getSensorXOffset()
        offsetY = self.__config['locations'][sensorId]['y'] + \
            self.getSensorYOffset()

        return {
            'offsetX': offsetX,
            'offsetY': offsetY
        }

    def getImage(self, image):
        return self.__config['images'][image]

    def getMqttIp(self):
        return self.__config['mqtt']['ip']

    def getMqttPort(self):
        return self.__config['mqtt']['port']

    def getMqttTopic(self):
        return self.__config['mqtt']['topic']

    def getXMultiplier(self):
        return self.__config['pixel_size_multiplier']['x']

    def getYMultiplier(self):
        return self.__config['pixel_size_multiplier']['y']

    def getSensorLocations(self):
        return self.__config['sensors']['locations']

    def getHistorianFolder(self):
        return self.__config['historian']['folder']

    def getHistorianFilePrefix(self):
        return self.__config['historian']['file_prefix']

    def getAverageHeatmapTemp(self):
        return self.__config['heatmap']['average temp']

    def getTempLimit(self):
        return self.__config['tempWarning']['maxTemp']

    def getOpeningTime(self):
        return self.__config["openingHours"]["openingTime"]

    def getClosingTime(self):
        return self.__config["openingHours"]["closingTime"]