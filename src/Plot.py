import cv2
import matplotlib.pyplot as plt
import time

class Plot:
    def __init__(self, config):
        self.config = config
        self.backgroundImage = self.__loadBackgroundImage()
        self.fig, self.ax = plt.subplots()
        self.__preparePlot()

    def __loadBackgroundImage(self):
        imagePath = self.config.getImage('room')
        # Read the image
        image = plt.imread(imagePath)
        # Resize the image
        image = cv2.resize(
            image, (self.config.getRoomX(), self.config.getRoomY())
        )

        return image

    def __preparePlot(self):
        self.__createPlotFromBackgroundImage(self.backgroundImage)
        sensorLocations = self.__combineSensorLocations()
        self.__plotSensorLocations(sensorLocations)
        plt.show(block=False)
        plt.pause(0.1)
        self.cachedBackground = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        # self.ax.draw_artist(self.ln)
        self.fig.canvas.blit(self.fig.bbox)

    def blit(self, objectList):
        seperateList = self.__objectListToSeperateList(objectList)
        self.__plotHumans(seperateList)
        self.fig.canvas.restore_region(self.cachedBackground)
        self.ax.draw_artist(self.ln)
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()

    def __createPlotFromBackgroundImage(self, backgroundImage):
        plt.imshow(backgroundImage, extent=[0, self.config.getRoomX(), 0, self.config.getRoomY()])

    def __combineSensorLocations(self):
        locations = self.config.getSensorLocations()
        sensorLocations = {
            'x': [],
            'y': []
        }

        for location in locations:
            sensorLocations['x'].append(location['x'])
            sensorLocations['y'].append(location['y'])

        return sensorLocations

    def __plotSensorLocations(self, sensorLocations):
        plt.plot(sensorLocations['x'], sensorLocations['y'], 'g.', markersize=8)

    def __plotHumans(self, seperateList):
        if(len(seperateList) > 0 and len(seperateList['x']) > 0):
            (self.ln,) = self.ax.plot(seperateList['x'], seperateList['y'], 'bX', markersize=12, animated=True)
            self.ln.set_visible(True)
        else:
            self.ln.set_visible(False)


    def __objectListToSeperateList(self, objectList):
        seperateLists = {}

        for obj in objectList:
            keys = [*obj]
            for key in keys:
                if(not key in seperateLists):
                    seperateLists[key] = []

                seperateLists[key].append(obj[key])

        seperateList = seperateLists
        return seperateLists