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
inputPin = 24
shutoffPin = 12
numImages = 50

#setup for all the pins
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(shutoffPin, GPIO.OUT)
GPIO.setup(inputPin, GPIO.IN)

#after wakeup, wait for some seconds to give the other pi time to start up
sleep(10)

# wait to start recording until we get the signal from the other PI
#otherwise we just get some data anyways regardless of the signal we get
while recordWaitTime > 0: 
  if GPIO.input(inputPin):
    break
  sleep(1)


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



#check if the GPIO from the other raspi is low, that means it is done recording
#if it is, then send a signal to the timer board to stop the power
#check if the GPIO from the other raspi is low, that means it is done recording
#if it is, then send a signal to the timer board to stop the power, otherwise do nothing,
#the other board will handle the shutoff
while GPIO.input(inputPin):
  GPIO.output(shutoffPin,GPIO.HIGH)
  sleep(0.5)