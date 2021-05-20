from datetime import date
import time
import csv
import os


class Historian:
    def __init__(self, historianFolder, historianFilePrefix, headerFields):
        self.__historianFolder = historianFolder
        self.__historianFilePrefix = historianFilePrefix
        self.__path = self.__constructFilePath(
            self.__historianFolder, self.__historianFilePrefix)
        self.__current_date = None
        self.__field_names = headerFields

    def __constructFilePath(self, folder, file_prefix):
        # create path to file
        filename = file_prefix + '-' + self.__getCurrentDateAsString() + '.csv'
        return os.path.join(folder, filename)

    def __getCurrentDateAsString(self):
        # current date
        return str(date.today())

    def __writeHeader(self):
        # create headers
        with open(self.__path, 'w',  newline='') as historianFile:
            writer = csv.DictWriter(
                historianFile, fieldnames=self.__field_names)
            writer.writeheader()
            historianFile.close()

    def writeCoordinatesToFile(self, sensorId, x, y):
        # get date, if new: write headers
        if self.__current_date != self.__getCurrentDateAsString():
            self.__writeHeader()
            self.__current_date = self.__getCurrentDateAsString()

        coordinatesObject = {
            # get sensor, coordinates and timestamp
            'id': sensorId,
            'x': x,
            'y': y,
            'timestamp': time.time()
        }

        with open(self.__path, 'a', newline='') as historianFile:
            # write to file
            writer = csv.DictWriter(
                historianFile, fieldnames=self.__field_names)
            writer.writerow(coordinatesObject)
            historianFile.close()
