# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from time import sleep
import board
import adafruit_dht
import csv
import datetime
import os.path
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D21)

datafile = "/home/pi/Artemis/Dashboard/assets/data/TempHumid.csv"
#open csv file and append temp data to it
#f = open('')

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

#get temp and humidity and add to 'data' dictionary
def get_data():
    now = datetime.datetime.now()
    temperature = dhtDevice.temperature * (9 / 5) - 32
    humidity = dhtDevice.humidity
    if humidity is not None and temperature is not None:
        data = {'timestamp':str(now.strftime("%Y%m%d_%H-%M-%S")), 'temperature':temperature, 'humidity':humidity}
        print(data)
        return(data)
    else:
        data = {'timestamp':None, 'temperature':None, 'humidity': None}
        print(data)
        return(data)

#write temp, humidity and time stamps to csv file
def add_to_file(data):
    if os.path.isfile(datafile): #checks if file exists. if yes, appends values for dictionary under corresponding header in a new line
        with open(datafile, 'a', newline='') as csvfile: 
            fieldnames = ['Time', 'Temperature', 'Humidity']
            data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            data_writer.writerow({'Time': data['timestamp'], 'Temperature': data['temperature'], 'Humidity': data['humidity']})
    
    else: #creates file (that has been checked and does not yet exist) and adds headers and values for all 3 keys in dict
        with open(datafile, 'w', newline='') as csvfile: 
            fieldnames = ['Time', 'Temperature', 'Humidity']
            data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            data_writer.writeheader()
            data_writer.writerow({'Time': data['timestamp'], 'Temperature': data['temperature'], 'Humidity': data['humidity']})



while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        data = get_data()
        if data is not None:
            add_to_file(data)
        sleep(10)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
