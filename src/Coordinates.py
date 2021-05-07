class Coordinates:
    def __init__(self, config):
        self.config = config

    def removeDuplicates(self, sensorList):
        allXY = []
        for sensorId in sensorList:
            allXY = allXY + self.__getXYFromSensor(sensorList[sensorId])

        return self.__checkOverlap(allXY)
        

    def __getXYFromSensor(self, sensor):
        tempXY = []

        for i in range(0, len(sensor.getX())):
            tempXY.append({
                'x': sensor.getX()[i],
                'y': sensor.getY()[i]
            })

        return tempXY

    def __checkOverlap(self, allXY):
        maxDifference = self.config.getMaxDifference()
        for coordinate in allXY:
            tempAllXY = allXY.copy()
            tempAllXY.remove(coordinate) # Remove itself

            for test_coordinate in tempAllXY:
                if (
                    (
                        test_coordinate['x'] <= (coordinate['x'] + maxDifference) and
                        test_coordinate['x'] >= (coordinate['x'] - maxDifference)
                    ) and (
                        test_coordinate['y'] <= (coordinate['y'] + maxDifference) and
                        test_coordinate['y'] >= (coordinate['y'] - maxDifference)
                    )
                ):
                    allXY.remove(coordinate)
                    break

        return allXY
