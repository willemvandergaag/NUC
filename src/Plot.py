from SensorList import SensorList
from Sensor import Sensor
import cv2
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


class Plot:
    def __init__(self, roomX, roomY, sensorLocations, image, tempLimit):
        self.__roomX = roomX
        self.__roomY = roomY
        self.__sensorLocations = sensorLocations
        self.__image = image
        self.__tempLimit = tempLimit
        self.__backgroundImage = self.__loadBackgroundImage()
        self.__figure, self.__ax = plt.subplots()
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
        self.__createLegend()
        self.__createText()
        plt.show(block=False)
        plt.pause(0.1)
        self.__cachedBackground = self.__figure.canvas.copy_from_bbox(
            self.__figure.bbox)
        self.__figure.canvas.blit(self.__figure.bbox)

    def draw(self, seperateList, sensorList: SensorList):
        self.__plotHumans(seperateList)
        self.__writeHumanLocations(seperateList)
        self.__drawTempWarnings(sensorList)
        self.__figure.canvas.restore_region(self.__cachedBackground)
        if hasattr(self, '_' + self.__class__.__name__ + '__human'):
            self.__ax.draw_artist(self.__human)
            for location in self.__humanLocations:
                self.__ax.draw_artist(location)
        self.__figure.canvas.blit(self.__figure.bbox)
        self.__figure.canvas.flush_events()

    def __createPlotFromBackgroundImage(self, backgroundImage):
        plt.imshow(backgroundImage, extent=[0, self.__roomX, 0, self.__roomY])

    def __combineSensorLocations(self):
        locations = self.__sensorLocations
        sensorLocations = {
            'x': [],
            'y': []
        }

        for location in locations:
            sensorLocations['x'].append(location['x'])
            sensorLocations['y'].append(location['y'])

        return sensorLocations

    def __plotSensorLocations(self, sensorLocations):
        plt.plot(sensorLocations['x'],
                 sensorLocations['y'], 'g.', markersize=8)

    def __plotHumans(self, seperateList):
        if(len(seperateList) > 0 and len(seperateList['x']) > 0):
            (self.__human,) = self.__ax.plot(
                seperateList['x'], seperateList['y'], 'bX', markersize=12, animated=True)
            self.__human.set_visible(True)
        else:
            if hasattr(self, '_' + self.__class__.__name__ + '__human'):
                self.__human.set_visible(False)

    def __writeHumanLocations(self, seperateList):
        # Offset creates a new row for every coordinate
        offsetText = 1
        self.__humanLocations = []
        for i_x, i_y in zip(seperateList['x'], seperateList['y']):
            self.__humanLocations.append(self.__ax.text(-220, 445 - (offsetText * 20), str(offsetText) +
                                                        ': ' + '({}, {})'.format(int(i_x), int(i_y))))
            offsetText = offsetText + 1

    def __createLegend(self):
        legend_elements = [Line2D([0], [0], marker='X', color='w', label='Person',
                                  markerfacecolor='b', markersize=15),
                           Line2D([0], [0], marker='.', color='w', label='Sensor',
                                  markerfacecolor='g', markersize=15),
                           Line2D([0], [0], marker='8', color='w', label='Very hot object',
                                  markerfacecolor='r', markersize=15)]
        plt.legend(handles=legend_elements, title='Symbols',
                   bbox_to_anchor=(1.05, 1), loc='upper left')

    def __createText(self):
        # display list of locations
        plt.text(-250, 445, 'Locations of people', weight='bold')

    def __createTempAlertList(self, sensorList):
        allTemps = []
        for sensorId in sensorList:
            allTemps = allTemps + self.__getTempAlerts(sensorList[sensorId])

        return allTemps

    def __getTempAlerts(self, sensor: Sensor):
        tempXY = [{
            'id': sensor.getId(),
            'tempAlert': sensor.getTempAlert()
        }]
        return tempXY

    def __detectTempAlerts(self, allTemps):
        sensorsDetectingTemp = []
        for sensor in allTemps:
            if sensor['tempAlert'] > self.__tempLimit:
                sensorsDetectingTemp.append(sensor['id'])
        return sensorsDetectingTemp

    def __drawTempWarnings(self, sensorList):
        allTempLimits = self.__createTempAlertList(sensorList)
        sensorsDetectingTemp = self.__detectTempAlerts(allTempLimits)
        tempWarningLocations = {
            'x': [],
            'y': []
        }
        if sensorsDetectingTemp:
            for i in range(0, len(sensorsDetectingTemp)):
                for location in self.__sensorLocations:
                    if sensorsDetectingTemp[i] == location['id']:
                        tempWarningLocations['x'].append(location['x'])
                        tempWarningLocations['y'].append(location['y'])
        self.__plotTempAlerts(tempWarningLocations)

    def __plotTempAlerts(self, tempWarningLocations):
        print(tempWarningLocations)
        (self.__human,) = self.__ax.plot(
            tempWarningLocations['x'], tempWarningLocations['y'], 'r8', markersize=12)
