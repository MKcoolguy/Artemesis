import time
from time import sleep
import board
import csv
import datetime
import os.path
import RPi.GPIO as GPIO

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#Datafile Location
datafile = "/home/pi/Artemis/Dashboard/assets/data/temperature.csv"

#Fetch distance and timestamp
def get_data():
    now = datetime.datetime.now()

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    if distance is not None:
        data = {'timestamp': str(now.strftime(
            "%Y%m%d_%H-%M-%S")), 'distance': distance}
        print(data)
        return(data)
    else:
        data = {'timestamp': None, 'distance': None}
        print(data)
        return(data)

#Writes Distance and Time to .csv file
def add_to_file(data):
    # checks if file exists. if yes, appends values for dictionary under corresponding header in a new line
    if os.path.isfile(datafile):
        with open(datafile, 'a', newline='') as csvfile:
            fieldnames = ['Time', 'Distance']
            data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            data_writer.writerow(
                {'Time': data['timestamp'], 'Distance': data['distance']})

    else:  # creates file (that has been checked and does not yet exist) and adds headers and values for all 3 keys in dict
        with open(datafile, 'w', newline='') as csvfile:
            fieldnames = ['Time', 'Distance']
            data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            data_writer.writeheader()
            data_writer.writerow(
                {'Time': data['timestamp'], 'Distance': data['distance']})

#While script is active
while True:
    try:
        #Fetches the data to write it to the file
        data = get_data()
        print(data)
        if data is not None:
            add_to_file(data)
        sleep(10)

    except RuntimeError as error:
        # Errors happen fairly often, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        GPIO.cleanup()
        raise error

    time.sleep(2.0)
