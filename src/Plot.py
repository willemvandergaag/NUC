from Sensor import Sensor
import cv2
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from datetime import datetime


class Plot:
    def __init__(self, roomX, roomY, sensorLocations, image, tempLimit, getOpeningTime, getClosingTime, getSocialDistancing):
        self.__roomX = roomX
        self.__roomY = roomY
        self.__sensorLocations = sensorLocations
        self.__image = image
        self.__tempLimit = tempLimit
        self.__getOpeningTime = getOpeningTime
        self.__getClosingTime = getClosingTime
        self.__getSocialDistancing = getSocialDistancing
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
        # everything here is background, this is cached to make the code faster
        self.__createPlotFromBackgroundImage(self.__backgroundImage)
        sensorLocations = self.__combineSensorLocations()
        self.__plotSensorLocations(sensorLocations)
        self.__createLegend()
        self.__createText()
        plt.show(block=False)
        plt.pause(0.1)
        self.__cachedBackground = self.__figure.canvas.copy_from_bbox(
            self.__figure.bbox)
        self.__figure.canvas.manager.set_window_title('Workplace occupation and social distancing monitor ')
        self.__figure.canvas.blit(self.__figure.bbox)

    def draw(self, seperateList, sensorList):
        # these elements are loaded every loop
        # check if the list is not empty
        if('x' in seperateList and len(seperateList['x']) > 0):
            self.__plotHumans(seperateList)
            self.__writeHumanLocations(seperateList)
            self.__measureDistancesHumans(seperateList)
        else:
            if hasattr(self, '_' + self.__class__.__name__ + '__human'):
                # sit visibility to false
                self.__human.set_visible(False)

        self.__drawTempAlerts(sensorList)
        self.__figure.canvas.restore_region(self.__cachedBackground)
        # only if hummans are detected
        if hasattr(self, '_' + self.__class__.__name__ + '__human'):
            self.__ax.draw_artist(self.__human)
            # write locations of human
            for location in self.__humanLocations:
                self.__ax.draw_artist(location)
            # write distances between human
            for distance in self.__humanDistances:
                self.__ax.draw_artist(distance)
            # check if humans are detected during closing hours
            if self.__checkAfterhours():
                self.__ax.draw_artist(self.__afterhoursWarning)
        # draw temp alerts
        self.__ax.draw_artist(self.__tempAlerts)
        self.__figure.canvas.blit(self.__figure.bbox)
        self.__figure.canvas.flush_events()

    def __createPlotFromBackgroundImage(self, backgroundImage):
        # load background
        plt.imshow(backgroundImage, extent=[0, self.__roomX, 0, self.__roomY])

    def __combineSensorLocations(self):
        locations = self.__sensorLocations
        sensorLocations = {
            'x': [],
            'y': []
        }
    	# all x and y coordinates are grouped together
        for location in locations:
            sensorLocations['x'].append(location['x'])
            sensorLocations['y'].append(location['y'])

        return sensorLocations

    def __plotSensorLocations(self, sensorLocations):
        # draw locations of sensors
        plt.plot(sensorLocations['x'],
                 sensorLocations['y'], 'g.', markersize=8)

    def __plotHumans(self, seperateList):
        # draw locations of humans
        # only if there are humans
        if(len(seperateList) > 0 and len(seperateList['x']) > 0):
            (self.__human,) = self.__ax.plot(
                seperateList['x'], seperateList['y'], 'bX', markersize=12, animated=True)
            self.__human.set_visible(True)

    def __writeHumanLocations(self, seperateList):
        # Offset creates a new row for every coordinate
        offsetText = 1
        self.__humanLocations = []
        # zip combines the x and y components
        for i_x, i_y in zip(seperateList['x'], seperateList['y']):
            # the location is printed and the offset places the loactions beneath each other
            self.__humanLocations.append(self.__ax.text(-220, 445 - (offsetText * 20), str(offsetText) +
                                                        ': ' + '({}, {})'.format(int(i_x), int(i_y))))
            offsetText = offsetText + 1

    def __createLegend(self):
        # the legend shows the symbols and their meaning
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
        plt.text(-250, 240, 'Distance', weight='bold')

    def __createTempAlertList(self, sensorList):
        # all temperatures are collected
        allTemps = []
        for sensorId in sensorList:
            allTemps = allTemps + self.__getTempAlerts(sensorList[sensorId])

        return allTemps

    def __getTempAlerts(self, sensor: Sensor):
        # temp alert is collected per sensor
        tempXY = [{
            'id': sensor.getId(),
            'tempAlert': sensor.getTempAlert()
        }]
        return tempXY

    def __compareTempAlerts(self, allTemps):
        # tempalerts are compared to the limit, if they are above they are appended
        sensorsDetectingTemp = []
        for sensor in allTemps:
            if sensor['tempAlert'] > self.__tempLimit:
                sensorsDetectingTemp.append(sensor['id'])
        return sensorsDetectingTemp

    def __drawTempAlerts(self, sensorList):
        allTempLimits = self.__createTempAlertList(sensorList)
        sensorsDetectingTemp = self.__compareTempAlerts(allTempLimits)
        tempWarningLocations = {
            'x': [],
            'y': []
        }
        # if there are the sensors above the templimit these are plotted
        if sensorsDetectingTemp:
            for i in range(0, len(sensorsDetectingTemp)):
                for location in self.__sensorLocations:
                    if sensorsDetectingTemp[i] == location['id']:
                        tempWarningLocations['x'].append(location['x'])
                        tempWarningLocations['y'].append(location['y'])
        self.__plotTempAlerts(tempWarningLocations)

    def __plotTempAlerts(self, tempWarningLocations):
        # sensors above the limit get a new symbol
        (self.__tempAlerts,) = self.__ax.plot(
            tempWarningLocations['x'], tempWarningLocations['y'], 'r8', markersize=12)

    def __measureDistancesHumans(self, seperateList):
        # put coordinates in an array and calculate distances
        allCoordinates = self.__mergeCoordinatesToArray(seperateList)
        self.__calculateDistances(allCoordinates)

    def __calculateDistances(self, allCoordinates):
        # number for text
        coordinateNumber = 1
        self.__humanDistances = []
        rowNumber = 1
        for coordinate in allCoordinates:
            # compare to the next number
            compareNumber = coordinateNumber + 1
            # copy coordinates
            tempCoordinates = allCoordinates.copy()
            # remove current coordinate from temp list
            tempCoordinates.remove(coordinate)
            # compare to all other coordinates
            for testCoordinate in tempCoordinates:
                # calculate difference between x and y coordinates
                xDistance = abs(testCoordinate['x'] - coordinate['x'])
                yDistance = abs(testCoordinate['y'] - coordinate['y'])
                # pythagoras
                XYdistance = int(
                    math.sqrt(xDistance * xDistance + yDistance * yDistance))
                textColor = 'black'
                # if these people are to close together, the distance is in red
                if XYdistance < self.__getSocialDistancing:
                    textColor = 'red'
                # print
                self.__humanDistances.append(self.__ax.text(-220, 240 - (rowNumber * 20), str(coordinateNumber) +
                                                            ' & ' + str(compareNumber) + ' = ' + str(XYdistance), color=textColor))
                compareNumber += 1
                rowNumber += 1
            allCoordinates.remove(coordinate)
            coordinateNumber += 1

    def __mergeCoordinatesToArray(self, seperateList):
        # put all coordinates in an array
        allCoordinates = []
        for i_x, i_y in zip(seperateList['x'], seperateList['y']):
            allCoordinates.append({
                'x': i_x,
                'y': i_y
            })
        return allCoordinates

    def __checkAfterhours(self):
        # Returns a datetime object containing the local date and time
        dateTimeObj = datetime.now()
        # if a person is detected while the office is closed, display this
        if dateTimeObj.hour >= self.__getClosingTime or dateTimeObj.hour < self.__getOpeningTime:
            self.__afterhoursWarning = self.__ax.text(335, 100, 'Person detected\nafter hours!', weight='bold', color='red',
                                                      bbox=dict(facecolor='none', edgecolor='red'))
            return True
        else:
            return False
