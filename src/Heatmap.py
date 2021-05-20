from os import sep
import numpy as np
import math
import cv2


class Heatmap:
    def __init__(self, averageHeatmapTemp, roomX, roomY, xMultiplier, yMultiplier):
        self.__averageHeatmapTemp = averageHeatmapTemp
        self.__roomX = roomX
        self.__roomY = roomY
        self.__xMultiplier = xMultiplier
        self.__yMultiplier = yMultiplier

    def __createEmptyMap(self):
        # create an array the size of the room filles with the average temp
        heatmapArray = [self.__averageHeatmapTemp] * \
            (self.__roomX * self.__roomY)
        heatmapArray = np.asarray(heatmapArray)
        # resize the array
        heatmapArray = heatmapArray.reshape(self.__roomY, self.__roomX)
        return heatmapArray

    def createHeatmap(self, seperateLists):
        heatmapArray = self.__createEmptyMap()
        heatmapArray = self.__modifyHeatmap(heatmapArray, seperateLists)
        img = self.__createImageCV(heatmapArray)
        #display heatmap
        cv2.imshow('Heatmap', img)

    def __modifyHeatmap(self, heatmapArray, seperateLists):
        xArray = seperateLists['x']
        yArray = seperateLists['y']

        for i in range(0, len(xArray)):
            # x and y are center person in cm
            #  [0][0] = top left
            x = xArray[i]
            y = self.__roomY - yArray[i]

            # create starting point heatmap
            # starting point is top left corner of the map in cm
            startx = int(x - seperateLists['heatmaps']
                         [i]['settings']['xSize'] * 4.8)
            if startx < 0:
                startx = 0
            starty = int(y - seperateLists['heatmaps']
                         [i]['settings']['ySize'] * 3.5)
            if starty < 0:
                startx = 0

            # temperatures are collected and placed in a array with the correct dimension
            tempsList = seperateLists['heatmaps'][i]['temps']
            # make an array out of the list
            tempsArray = np.asarray(tempsList)
            # reshape to proper dimensions
            tempsArray = tempsArray.reshape(
                (seperateLists['heatmaps'][i]['settings']['ySize'], seperateLists['heatmaps'][i]['settings']['xSize']))

            # flip the image left-right
            tempsArray = np.fliplr(tempsArray)

            # array is enlarged to cm in stead of pixels
            tempsArray = np.kron(tempsArray, np.ones(
                (int(self.__xMultiplier), int(self.__yMultiplier))))

            # temps in array are replaced bij temps from sensor
            for yTemp in range(0, len(tempsArray)):
                for xTemp in range(0, len(tempsArray[0])):
                    heatmapArray[starty + yTemp][startx +
                                                 xTemp] = tempsArray[yTemp][xTemp]

        return heatmapArray

    def __createImageCV(self, heatmapArray):
        # find min value, subtract this from all values
        minValue = math.floor(np.amin(heatmapArray))
        maxValue = math.ceil(np.amax(heatmapArray))
        heatmapComplete = heatmapArray - minValue

        # Now scaled to 0 - 255
        if minValue != maxValue:
            heatmapComplete = heatmapComplete * 255 / (maxValue - minValue)

        # apply colormap
        imageGray = heatmapComplete.astype(np.uint8)
        image = cv2.applyColorMap(imageGray, cv2.COLORMAP_JET)

        return image
