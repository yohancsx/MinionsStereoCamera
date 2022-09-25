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
recordWaitTime = 10
recordTime = 10
lightDelayTime = 3
shutoffPin = 12

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