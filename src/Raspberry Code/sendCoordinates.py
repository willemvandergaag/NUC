from numpy import loadtxt

from pylab import *
from scipy.ndimage import measurements
import math
import time
import board
import busio
import adafruit_mlx90640
import paho.mqtt.publish as publish
import json

config = json.load(
    open('/home/pi/Desktop/config.json')
    )

sensor = config['sensorId']
frameWidth = config['sensorPixels']['width']
frameHeight = config['sensorPixels']['height']
upperTempHuman = config['humanTemps']['upperLimit']
lowerTempHuman = config['humanTemps']['lowerLimit']
lowerArea = config['areaLimits']['upperLimit']
topic = config['MQTT']['topic']
ip = config['MQTT']['ip']


# data string to compare
datastringOld = ''
# i2c settings
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])
# refrech rate
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
# loop
while True:
    stamp = time.monotonic()
    humansDetected = 0
    xc = []
    yc = []
    highTemp = 0
    frame = [0] * (frameHeight * frameWidth)
    try:
        # get frame
        mlx.getFrame(frame)
    except:
        # these happen, no biggie - retry
        continue
    # round to ints
    frame = [int(round(num)) for num in frame]
    # detect dead pixels
    for temp in frame:
        if temp == -273:
            temp = 21
    frameTemps = frame
    # reshape frame
    frameTemps = np.reshape(frameTemps, (frameWidth, frameHeight))
    for h in range(frameWidth):
        for w in range(frameHeight):
            if frame[h * frameHeight + w] > highTemp:
                # check if this is the highest temperature
                highTemp = frame[h * frameHeight + w]
            # check if temperature is outside the limits of a human
            if frame[h * frameHeight + w] < lowerTempHuman or frame[h * frameHeight + w] > upperTempHuman:
                # set to 0
                frame[h * frameHeight + w] = 0
            else:
                # set to 1
                frame[h * frameHeight + w] = 1
    frameEdit = frame 
    frameEdit = np.reshape(frameEdit, (frameWidth, frameHeight))
    
    # make clusters
    lw, num = measurements.label(frameEdit)
    coordinates = lw
    clusters = {} # empty clusters object
    row_num = 0 # row number starts at

    # place a x and y of every number in the array
    for row in coordinates:
        cel_num = 0 # cel_num reset for new row
        for cel in row:
            # 0 doesnt have a value
            # if it exists, +1 otherwise =1
            if cel > 0:
                if str(cel) not in clusters:
                    clusters[str(cel)] = []
                clusters[str(cel)].append({'x': cel_num, 'y': row_num})
            cel_num += 1 # next cel
        row_num += 1 # next row

    # loop through every "clusternumber"
    heatmap = []
    for cluster_num, cluster_val in clusters.items():
        all_x = [] # every cluster an empty array
        all_y = [] # every cluster an empty array
        for element in cluster_val:
            all_x.append(element['x']) # add all x's to array
            all_y.append(element['y']) # add all y's to array

        x_min = min(all_x) # min x
        x_max = max(all_x) # max x
        y_min = min(all_y) # min y
        y_max = max(all_y) # max y
        x_gem = frameHeight - ((x_min + x_max) / 2) # average X
        y_gem = (y_min + y_max) / 2 # average y

        # every pixel is 1
        area = len(all_x)
        # check if it is large enough
        if(area > lowerArea):
            # append coordinates
            xc = np.append(xc, x_gem)
            yc = np.append(yc, y_gem)
            humansDetected += 1
            temperatures = []
            # find temperatures of detected person
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    temperatures.append(int(frameTemps[y][x]))
            # create heatmap of area where person is detected
            heatmap.append({
                "settings": {
                    "xSize": x_max - x_min + 1,
                    "ySize": y_max - y_min + 1
                    },
                "temps": temperatures
            })            
        
    clusters = []
    # append all humans
    for i in range(0, len(xc)):
        # print(xc[i], yc[i])
        clusters.append({
            "coordinates":{ 
                "x": xc[i],
                "y": yc[i]
                },
            "heatmaps": heatmap[i]
        })
    
    data = {
        "data": {
            "sensor": sensor,
            "humans": humansDetected,
            "tempAlert": highTemp,
            "clusters": clusters,
        }
    }
    
    datastring = json.dumps(data)
    # if connection is lost, try for 60s
    attempts = 0
    # check if something new is detectedg
    if(datastringOld != datastring):
        while attempts < 60:
            try:
                # write to MQTT broker
                publish.single(topic, datastring, hostname = ip)
                print("Sensor read and sent in %0.2f s" % (time.monotonic() - stamp))
                break
            except:
                # if connection fails
                print("Connection to MQTT Broker failed, retrying in 1 second...")
                attempts = attempts + 1
                time.sleep(1)
    #datastring used for comparison
    datastringOld = datastring




