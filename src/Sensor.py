class Sensor:
    def __init__(self, config):
        self.config = config
        self.id = 0
        self.offsetX = 0
        self.offsetY = 0
        self.x = []
        self.y = []
        self.humans = 0
        self.heatmaps = []
        self.tempAlert = False

    def getOffsetX(self):
        return self.offsetX
    
    def setOffsetX(self, offset):
        self.offsetX = self.__getLocationBySensorId()['x'] - offset

    def getOffsetY(self):
        return self.offsetY
    
    def setOffsetY(self, offset):
        self.offsetY = self.__getLocationBySensorId()['y'] + offset

    def convertXPixelToCentimeters(self, pixelX):
        return (
            self.getOffsetX() + (pixelX - 1) * self.config.getXMultiplier()
        )
    
    def __getLocationBySensorId(self):
        locations = self.config.getSensorLocations()
        for location in locations:
            if location['id'] == self.getId():
                return location

    def convertYPixelToCentimeters(self, pixelY):
        return (
            self.getOffsetY() - (pixelY - 1) * self.config.getYMultiplier()
        )

    def getX(self):
        return self.x

    def appendToX(self, data):
        self.x.append(
            self.convertXPixelToCentimeters(data)
        )
    
    def getY(self):
        return self.y
    
    def appendToY(self, data):
        self.y.append(
            self.convertYPixelToCentimeters(data)
        )

    def getHumans(self):
        return self.humans

    def setHumans(self, humans):
        self.humans = humans

    def getHeatmaps(self):
        return self.heatmaps

    def setHeatmaps(self, data):
        self.heatmaps.append(data)

    def getTempAlert(self):
        return self.tempAlert
    
    def setTempAlert(self, data):
        self.tempAlert = data

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
    