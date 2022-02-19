#Tests a simple loop to catch 10 pictures.
#Files are named image000X where X would begin the increment.
#Source code from the official PiCamera package
#http://picamera.readthedocs.io

from picamera import PiCamera

camera = PiCamera()

#main body
try:
    for i in range(10):
        camera.capture('/home/pi/Camera/image{0:04d}.jpg'.format(i))
    pass
except:
    print("Exception thrown, unknown error.")
finally:
    camera.close()