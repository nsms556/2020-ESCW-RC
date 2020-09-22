from time import time, sleep

import rcutils.RCUtils as util
from rcutils.RCStatic import *
import rcutils.GPIO as GPIO

class Car :
    def __init__(self) :
        self.GPIOCtrl = GPIO.GPIOAdapter()
        self.shift = SHIFT_STOP
        self.speed = 0
        self.steer = STEER_STRAIGHT
        self.headLight = LED_OFF 
        self.breakLight = LED_ON
        self.backLight = LED_ON
        self.cruise = CRUISE_OFF
        self.backDis = BACKDISTANCE_UNKNOWN
        self.HLCtrlTime = time()
        self.CRCtrlTime = time()
        self.quitCtrl = False

    def __del__(self) :
        del(self.GPIOCtrl)

    def setShift(self, status) :
        self.shift = status

    def getShift(self) :
        return self.shift

    def setSpeed(self, value) :
        self.speed = value

    def getSpeed(self) :
        return self.speed

    def setSteer(self, value) :
        self.steer = value

    def getSteer(self) :
        return self.steer

    def setHeadLight(self, status, ctrlTime) :
        self.headLight = status
        self.HLCtrlTime = ctrlTime

    def getHeadLight(self) :
        return self.headLight

    def setBreakLight(self, status) :
        self.breakLight = status

    def getBreakLight(self) :
        return self.breakLight

    def setBackLight(self, status) :
        self.backLight = status

    def getBackLight(self) :
        return self.backLight

    def setCruise(self, status, ctrlTime) :
        self.cruise = status
        self.CRCtrlTime = ctrlTime
                
    def getCruise(self) :
        return self.cruise

    def setBackDistance(self) :
        startTime = None

        self.GPIOCtrl.runWaveTrigger()

        try :
            timeOut = time()
            while self.GPIOCtrl.getWaveEcho() == False :
                startTime = time()
                if (startTime - timeOut) * 1000000 >= WAVE_MAX_DURATION :
                    raise Exception
            
            timeOut = time()
            while self.GPIOCtrl.getWaveEcho() == True :
                endTime = time()
                if (endTime - timeOut) * 1000000 > WAVE_MAX_DURATION :
                    raise Exception

            travelTime = endTime - startTime
            value = util.waveTimeToDis(travelTime)

            if value < WAVE_MAX_DISTANCE :
                pass
            else :
                value = BACKDISTANCE_UNKNOWN
        except Exception :
            value = BACKDISTANCE_UNKNOWN
        finally :
            self.backDis = value

    def getBackDistance(self) :
        return self.backDis

    def getHLCtrlTime(self) :
        return self.HLCtrlTime
    
    def getCRCtrlTime(self) :
        return self.CRCtrlTime

    def setQuitCtrl(self, status) :
        self.quitCtrl = status

    def getQuitCtrl(self) :
        return self.quitCtrl

    def drive(self) :
        if self.getQuitCtrl() == True :
            raise util.QuitException

        self.setBackDistance()
        if self.getBackDistance() != BACKDISTANCE_UNKNOWN :
            if self.getBackDistance() < BACKDISTANCE_MINIMUM and self.getShift() == SHIFT_BACKWARD :
                self.setCruise(CRUISE_OFF)
                self.setShift(SHIFT_STOP)

        if self.getCruise() == CRUISE_ON :
            self.setShift(SHIFT_FORWARD)

        if self.getShift() == SHIFT_FORWARD :
            self.setBreakLight(LED_OFF)
        elif self.getShift() == SHIFT_BACKWARD :
            self.setBreakLight(LED_ON)
        else :
            self.setBreakLight(LED_ON)

        self.GPIOCtrl.setDC(self.getShift())
        self.GPIOCtrl.setServo(util.steerValueToSig(self.getSteer()))
        self.GPIOCtrl.headLightONOFF(self.getHeadLight())
        self.GPIOCtrl.breakLightONOFF(self.getBreakLight())
        self.GPIOCtrl.backLightONOFF(self.getBackLight())

if __name__ == "__main__":
    car = Car()

    while True :
        key = input('Press Key : ')

        if key == 'w' :
            car.setShift(SHIFT_FORWARD)
        if key == 'a' :
            car.setSteer(STEER_LEFTLIMIT)
        if key == 'd' :
            car.setSteer(STEER_RIGHTLIMIT)
        if key == 's' :
            car.setShift(SHIFT_STOP)
        if key == 'x' :
            car.setShift(SHIFT_BACKWARD)
        if key == 'e' :
            car.setHeadLight(LED_OFF, time())
        if key == 'r' :
            car.setHeadLight(LED_ON, time())
        if key == 'q' :
            car.setQuitCtrl(True)

        try :
            car.drive()
        except Exception :
            del(car)
            break

    print('RCCAR POWER OFF')
