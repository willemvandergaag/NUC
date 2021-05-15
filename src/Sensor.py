class Sensor:
    def __init__(self, xMultiplier, yMultiplier, sensorLocations):
        self.__xMultiplier = xMultiplier
        self.__yMultiplier = yMultiplier
        self.__sensorLocations = sensorLocations
        self.__id = 0
        self.__offsetX = 0
        self.__offsetY = 0
        self.__x = []
        self.__y = []
        self.__humans = 0
        self.__heatmaps = []
        self.__tempAlert = 0

    def getOffsetX(self):
        return self.__offsetX
    
    def setOffsetX(self, offset):
        self.__offsetX = self.__getLocationBySensorId()['x'] - offset

    def getOffsetY(self):
        return self.__offsetY
    
    def setOffsetY(self, offset):
        self.__offsetY = self.__getLocationBySensorId()['y'] + offset

    def convertXPixelToCentimeters(self, pixelX):
        return (
            self.getOffsetX() + (pixelX - 1) * self.__xMultiplier
        )
    
    def __getLocationBySensorId(self):
        locations = self.__sensorLocations
        for location in locations:
            if location['id'] == self.getId():
                return location

    def convertYPixelToCentimeters(self, pixelY):
        return (
            self.getOffsetY() - (pixelY - 1) * self.__yMultiplier
        )

    def getX(self):
        return self.__x

    def appendToX(self, data):
        self.__x.append(
            self.convertXPixelToCentimeters(data)
        )
    
    def getY(self):
        return self.__y
    
    def appendToY(self, data):
        self.__y.append(
            self.convertYPixelToCentimeters(data)
        )

    def getHumans(self):
        return self.__humans

    def setHumans(self, humans):
        self.__humans = humans

    def getHeatmaps(self):
        return self.__heatmaps

    def setHeatmaps(self, data):
        self.__heatmaps = data

    def getTempAlert(self):
        return self.__tempAlert
    
    def setTempAlert(self, data):
        self.__tempAlert = data

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id = id
    