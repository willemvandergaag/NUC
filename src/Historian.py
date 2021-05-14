from datetime import date
import time
import csv
import os
import Config

class Historian:
    def __init__(self, config: Config):
        self.__path = self.__constructFilePath(config.getHistorianFolder(), config.getHistorianFilePrefix())
        self.__current_date = None
        self.__field_names = ['x', 'y', 'timestamp']

    def __constructFilePath(self, folder, file_prefix):
        filename = file_prefix + '-' + self.__getCurrentDateAsString() + '.csv'
        return os.path.join(folder, filename)

    def __getCurrentDateAsString(self):
        return str(date.today())

    def __writeHeader(self):

        with open(self.__path, 'w',  newline='') as historianFile:
            writer = csv.DictWriter(historianFile, fieldnames=self.__field_names)
            writer.writeheader()
            historianFile.close()        

    def writeCoordinatesToFile(self, x ,y):
        if self.__current_date != self.__getCurrentDateAsString():
            self.__writeHeader()
            self.__current_date = self.__getCurrentDateAsString()
        
        coordinatesObject = {
            'x': x,
            'y': y,
            'timestamp': time.time()
        }

        with open(self.__path, 'a', newline='') as historianFile:
            writer = csv.DictWriter(historianFile, fieldnames=self.__field_names)
            writer.writerow(coordinatesObject)
            historianFile.close()