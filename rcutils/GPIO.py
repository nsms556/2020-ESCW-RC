from time import sleep

import Jetson.GPIO as GPIO

from rcutils.RCStatic import *

class GPIOAdapter :
    pinlist = [DC_ENA, DC_IN1, DC_IN2, SERVO,
               HEADLIGHT, BACKLIGHT, BREAKLIGHT,
               WAVE_TRIG, WAVE_ECHO]

    def __init__(self) :
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(DC_ENA, GPIO.OUT)
        GPIO.setup(DC_IN1, GPIO.OUT)
        GPIO.setup(DC_IN2, GPIO.OUT)
        GPIO.setup(SERVO, GPIO.OUT)
        GPIO.setup(HEADLIGHT, GPIO.OUT)
        GPIO.setup(BACKLIGHT, GPIO.OUT)
        GPIO.setup(BREAKLIGHT, GPIO.OUT)
        GPIO.setup(WAVE_TRIG, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(WAVE_ECHO, GPIO.IN)

        self.servo = GPIO.PWM(SERVO, 50)
        self.servo.start(8)

    def __del__(self) :
        for pin in self.pinlist :
            if pin == SERVO :
                self.setServo(8)
                self.servo.stop()
            elif pin == WAVE_ECHO :
                pass
            else :
                GPIO.output(pin, GPIO.LOW)

        GPIO.cleanup()

    def headLightONOFF(self, status) :
        GPIO.output(HEADLIGHT, status)

    def breakLightONOFF(self, status) :
        GPIO.output(BREAKLIGHT, status)

    def backLightONOFF(self, status) :
        GPIO.output(BACKLIGHT, status)

    def setDC(self, status) :
        if status == SHIFT_FORWARD :
            GPIO.output(DC_ENA, GPIO.HIGH)
            GPIO.output(DC_IN1, GPIO.HIGH)
            GPIO.output(DC_IN2, GPIO.LOW)
        elif status == SHIFT_BACKWARD :
            GPIO.output(DC_ENA, GPIO.HIGH)
            GPIO.output(DC_IN1, GPIO.LOW)
            GPIO.output(DC_IN2, GPIO.HIGH)
        elif status == SHIFT_STOP :
            GPIO.output(DC_ENA, GPIO.LOW)
            GPIO.output(DC_IN1, GPIO.LOW)
            GPIO.output(DC_IN2, GPIO.LOW)
    
    def setServo(self, value) :
        self.servo.ChangeDutyCycle(value)
        

    def setWaveTrig(self, status) :
        GPIO.output(WAVE_TRIG, status)

    def getWaveEcho(self) :
        return GPIO.input(WAVE_ECHO)

    def runWaveTrigger(self) :
        GPIO.output(WAVE_TRIG, False)
        sleep(0.000002)
        GPIO.output(WAVE_TRIG, True)
        sleep(0.00001)
        GPIO.output(WAVE_TRIG, False)

if __name__ == "__main__":
    try :
        GPIOCon = GPIOAdapter()

        # DC Motor TEST
        GPIOCon.setDC(SHIFT_FORWARD)
        sleep(1)
        GPIOCon.setDC(SHIFT_STOP)
        sleep(1)
        GPIOCon.setDC(SHIFT_BACKWARD)
        sleep(1)
        GPIOCon.setDC(SHIFT_STOP)
        sleep(1)

        # Servo TEST
        GPIOCon.setServo(8)
        sleep(1)
        GPIOCon.setServo(10)
        sleep(1)
        GPIOCon.setServo(5)
        sleep(1)
        GPIOCon.setServo(8)
        sleep(1)

        # LED TEST
        GPIOCon.setHeadLight(LED_ON)
        sleep(0.5)
        GPIOCon.setHeadLight(LED_OFF)
        sleep(1)
        GPIOCon.setHeadLight(LED_ON)
        sleep(0.5)
        GPIOCon.setHeadLight(LED_OFF)
        sleep(1)

        GPIOCon.setBreakLight(LED_ON)
        sleep(0.5)
        GPIOCon.setBreakLight(LED_OFF)
        sleep(1)
        GPIOCon.setBreakLight(LED_ON)
        sleep(0.5)
        GPIOCon.setBreakLight(LED_OFF)
        sleep(1)

        GPIOCon.setBackLight(LED_ON)
        sleep(0.5)
        GPIOCon.setBackLight(LED_OFF)
        sleep(1)
        GPIOCon.setBackLight(LED_ON)
        sleep(0.5)
        GPIOCon.setBackLight(LED_OFF)
        sleep(1)

        # WAVE TEST
        

    finally :
        # Delete Object
        del(GPIOCon)

        # Print Test Complete
        print('TEST COMPLETE')
