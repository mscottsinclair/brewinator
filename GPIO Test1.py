import RPi.GPIO as GPIO
import time

GPIO.cleanup(16)
GPIO.setmode(GPIO.BOARD) ## This is the pin number of the board not the ID printed on the Cobbler
GPIO.setup(16, GPIO.OUT)

def Blink(numTimes, speed):
    for i in range(0, numTimes):
        print("Turning on....")
        GPIO.output(16, True)
        time.sleep(speed)
        print("Turning off....")
        GPIO.output(16, False)
        time.sleep(speed)
    ## GPIO.cleanup

iterations = 5
speed = 5

Blink(int(iterations), float(speed))
