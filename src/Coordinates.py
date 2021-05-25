from SensorList import SensorList
from Sensor import Sensor


class Coordinates:
    def __init__(self, maxDifference):
        self.__maxDifference = maxDifference

    def removeDuplicates(self, sensorList: SensorList):
        # check distance between people and remove doubles
        allXY = []
        for sensorId in sensorList:
            allXY = allXY + self.__getXYFromSensor(sensorList[sensorId])

        return self.__checkOverlap(allXY)

    def __getXYFromSensor(self, sensor: Sensor):
        tempXY = []
        # return the x, y, id and heatmaps for each sensor
        for i in range(0, len(sensor.getX())):
            tempXY.append({
                'x': sensor.getX()[i],
                'y': sensor.getY()[i],
                'id': sensor.getId(),
                'heatmaps': sensor.getHeatmaps()[i]
            })

        return tempXY

    def __checkOverlap(self, allXY):
        # if the difference is smaller than the maximum they are considered to be the same person
        maxDifference = self.__maxDifference
        for coordinate in allXY:
            # create a temp to compare
            tempAllXY = allXY.copy()
            tempAllXY.remove(coordinate)  # Remove itself

            for test_coordinate in tempAllXY:
                if (
                    # if both the x and y component are within the maxdifference
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
                    # remove the coordinate
                    allXY.remove(coordinate)
                    break

        return allXY

    def objectListToSeperateList(self, objectList):
        # the single object list is converted to seperate lists
        seperateLists = {}

        for obj in objectList:
            keys = [*obj]
            for key in keys:
                # if the key is not yet created, it is created
                if(not key in seperateLists):
                    seperateLists[key] = []

                seperateLists[key].append(obj[key])
        return seperateLists
