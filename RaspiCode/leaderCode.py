#imports for camera, GPIO, datetime (for the timestamp) and timer functionality
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import datetime

#supress GPIO warnings
GPIO.setwarnings(False)

#start the camera
camera = PiCamera()

#some variables, such as the pin numbers things are connected to
#and the delay times
ledPin = 23
outputPin = 24
recordTime = 10
lightDelayTime = 3

#setup for all the pins
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(outputPin, GPIO.OUT)

#after wakeup, wait for some seconds to give the other pi time to start up
sleep(10)

#now we output a high GPIO signal and wait to start recording 
GPIO.output(outputPin, GPIO.HIGH)
sleep(5)


#set the filename and annotation
date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
videoName = '/home/pi/stereocamvids_' + date + '.h264'


#record for some amount of time
camera.annotate_text = videoName
camera.start_recording(videoName)

#delay for a second before turning on the light
sleep(lightDelayTime)
GPIO.output(ledPin, GPIO.HIGH)

#wait to record then turn off
sleep(recordTime - lightDelayTime)
camera.stop_recording()

#turn off the light, and set the GPIO to low
GPIO.output(ledPin, GPIO.LOW)

#extra sleep so one camera turns off before the other, this is optional
sleep(3)
GPIO.output(outputPin, GPIO.LOW)
