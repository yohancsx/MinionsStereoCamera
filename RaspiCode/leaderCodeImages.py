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
shutoffPin = 12
numImages = 50

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

#loop through and capture images
for i in range(numImages):
  #turn on the light
  GPIO.output(ledPin, GPIO.HIGH)

  #small delay
  sleep(0.5)

  imageName = '/home/pi/stereocamvids_' + date + str(i) + '.h264'
  camera.capture(imageName)

  #turn off the light
  GPIO.output(ledPin, GPIO.LOW)

#extra sleep so one camera turns off before the other, this is optional
sleep(3)
GPIO.output(outputPin, GPIO.LOW)

sleep(50)

#OPTIONAL: you can connect the leader to the timer module as well, and if the follower has not turned 
#the system off for some reason after some time, the leader can then turn everything off
GPIO.setup(shutoffPin, GPIO.OUT)
GPIO.output(shutoffPin, GPIO.HIGH)