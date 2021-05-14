import cv2
import matplotlib.pyplot as plt

class Plot:
    def __init__(self, roomX, roomY, sensorLocations, image):
        self.__roomX = roomX
        self.__roomY = roomY
        self.__sensorLocations = sensorLocations
        self.__image = image
        self.__backgroundImage = self.__loadBackgroundImage()
        self.__figure, self.ax = plt.subplots()
        self.__preparePlot()

    def __loadBackgroundImage(self):
        imagePath = self.__image
        # Read the image
        image = plt.imread(imagePath)
        # Resize the image
        image = cv2.resize(
            image, (self.__roomX, self.__roomY)
        )

        return image

    def __preparePlot(self):
        self.__createPlotFromBackgroundImage(self.__backgroundImage)
        sensorLocations = self.__combineSensorLocations()
        self.__plotSensorLocations(sensorLocations)
        plt.show(block=False)
        plt.pause(0.1)
        self.cachedBackground = self.__figure.canvas.copy_from_bbox(self.__figure.bbox)
        # self.ax.draw_artist(self.ln)
        self.__figure.canvas.blit(self.__figure.bbox)

    def draw(self, seperateList):
        self.__plotHumans(seperateList)
        self.__figure.canvas.restore_region(self.cachedBackground)
        self.ax.draw_artist(self.ln)
        self.__figure.canvas.blit(self.__figure.bbox)
        self.__figure.canvas.flush_events()

    def __createPlotFromBackgroundImage(self, backgroundImage):
        plt.imshow(backgroundImage, extent=[0, self.__roomX, 0, self.__roomY])

    def __combineSensorLocations(self):
        locations = self.__sensorLocations()
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