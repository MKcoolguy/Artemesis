import ASUS.GPIO as GPIO
import dht11
import datetime
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)

try:
        while True:
            result = instance.read()
            if result_is_valid():
                print("LAST VALID INPUT: " + str(datetime.now()))
                print("TEMPERATURE: %3.1f C" % result.temperature)
                print("HUMIDITY: %3.1f %%" % result.humidity)

            time.sleep(6)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()