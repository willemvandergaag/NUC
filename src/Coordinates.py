from SensorList import SensorList
from Sensor import Sensor


class Coordinates:
    def __init__(self, maxDifference):
        self.__maxDifference = maxDifference

    def removeDuplicates(self, sensorList: SensorList):
        allXY = []
        for sensorId in sensorList:
            allXY = allXY + self.__getXYFromSensor(sensorList[sensorId])

        return self.__checkOverlap(allXY)

    def __getXYFromSensor(self, sensor: Sensor):
        tempXY = []
        for i in range(0, len(sensor.getX())):
            tempXY.append({
                'x': sensor.getX()[i],
                'y': sensor.getY()[i],
                'id': sensor.getId(),
                'heatmaps': sensor.getHeatmaps()[0][i]
            })

        return tempXY

    def __checkOverlap(self, allXY):
        maxDifference = self.__maxDifference
        for coordinate in allXY:
            tempAllXY = allXY.copy()
            tempAllXY.remove(coordinate)  # Remove itself

            for test_coordinate in tempAllXY:
                if (
                    (
                        test_coordinate['x'] <= (coordinate['x'] + maxDifference) and
                        test_coordinate['x'] >= (
                            coordinate['x'] - maxDifference)
                    ) and (
                        test_coordinate['y'] <= (coordinate['y'] + maxDifference) and
                        test_coordinate['y'] >= (
                            coordinate['y'] - maxDifference)
                    )
                ):
                    allXY.remove(coordinate)
                    break

        return allXY

    def objectListToSeperateList(self, objectList):
        seperateLists = {}

        for obj in objectList:
            keys = [*obj]
            for key in keys:
                if(not key in seperateLists):
                    seperateLists[key] = []

                seperateLists[key].append(obj[key])
        return seperateLists
