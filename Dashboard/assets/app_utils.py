import time
from time import sleep
import board
import adafruit_dht
import csv
import datetime
import os.path


class Temperature:


    # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
    # SPDX-License-Identifier: MI
    # Initialize the dht device, with data pin connected to: 21

    global dhtDevice
    global datafile
    dhtDevice = adafruit_dht.DHT11(board.D21)
    # Datafile Location
    datafile = "/home/pi/Artemis/Dashboard/assets/data/temperature.csv"


    # Fetch temperature, time, and humidity
    def get_data():
        now = datetime.datetime.now()
        temperature = dhtDevice.temperature * 1.8 + 32
        humidity = dhtDevice.humidity
        if humidity is not None and temperature is not None:
            data = {'timestamp': str(now.strftime(
                "%Y%m%d_%H-%M-%S")), 'temperature': temperature}
            print(data)
            return (data)
        else:
            data = {'timestamp': None, 'temperature': None, 'humidity': None}
            print(data)
            return (data)


    # Writes Temperature and Time to .csv file
    def add_to_file(data):
        # checks if file exists. if yes, appends values for dictionary under corresponding header in a new line
        if os.path.isfile(datafile):
            with open(datafile, 'a', newline='') as csvfile:
                fieldnames = ['Time', 'Temperature']
                data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                data_writer.writerow(
                    {'Time': data['timestamp'], 'Temperature': data['temperature']})

        else:  # creates file (that has been checked and does not yet exist) and adds headers and values for all 3 keys in dict
            with open(datafile, 'w', newline='') as csvfile:
                fieldnames = ['Time', 'Temperature']
                data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                data_writer.writeheader()
                data_writer.writerow(
                    {'Time': data['timestamp'], 'Temperature': data['temperature']})


