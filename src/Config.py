import json

class Config:
    def __init__(self, file):
        self.config = {}

        self.__openFileToJSON(file)

    # Opens a configuration file
    # @return a JSON object
    def __openFileToJSON(self, file):
        self.config = json.load(
            open(file)
        )

    def getRoomX(self):
        return self.config['room']['width']

    def getRoomY(self):
        return self.config['room']['length']

    def getNumberOfSensors(self):
        return self.config['sensors']['number']

    def getMaxDifference(self):
        return self.config['humans']['max_offset']

    def getSensorXOffset(self):
        return self.config['sensors']['offset']['x']

    def getSensorYOffset(self):
        return self.config['sensors']['offset']['y']

    def getSensorOffsets(self, sensorId):
        # Sensors have a name from 1 upwards, arrays are 0-indexed
        sensorId = sensorId - 1
        offsetX = self.config['locations'][sensorId]['x'] - self.getSensorXOffset()
        offsetY = self.config['locations'][sensorId]['y'] + self.getSensorYOffset()

        return {
            'offsetX': offsetX,
            'offsetY': offsetY
        }

    def getImage(self, image):
        return self.config['images'][image]

    def getMqttIp(self):
        return self.config['mqtt']['ip']

    def getMqttPort(self):
        return self.config['mqtt']['port']
    
    def getMqttTopic(self):
        return self.config['mqtt']['topic']

    def getXMultiplier(self):
        return self.config['pixel_size_multiplier']['x']

    def getYMultiplier(self):
        return self.config['pixel_size_multiplier']['y']

    def getSensorLocations(self):
        return self.config['sensors']['locations']