from time import time, sleep

import cwiid as WII

import rcutils.Wiimote as Wiimote
import rcutils.Car as Car
from rcutils.WiiAdapter import WiiAdapter
from rcutils.RCStatic import *
import rcutils.RCUtils as util

import AIController
import cv2

wii = Wiimote.Wiimote()
car = Car.Car()
cam = util.cameraOpen()
adapter = WiiAdapter(wii)

autoMode = False
modeCtrlTime = time()

print('Loading AI Model...')
AI = AIController.AIController(cam, wii)

print('RC Power ON')
while True :
    try :
        if autoMode == DRIVE_AUTO :
            # Set Value from Auto to Car
            #print('Drive Auto')
            
            steer = AI.steerValue()
            shift = AI.shiftState(car.shift)

            # Performing State from TSRlist to Pop
            TSRlist = AI.runTSR()
            print('Found Sign : {}'.format(TSRlist))

            if wii.getButtonState() - WII.BTN_RIGHT == 0 :
                raise util.ModeException
        else :
            # Set Value from Wii to Car
            #print('Drive Manual')

            shift = adapter.shiftState()
            steer = adapter.steerValue()
            speed = adapter.speedValue(car.speed, car.shift, car.cruise)
            cruise, CRCtrlTime = adapter.cruiseState(car.cruise, car.speed,
                    car.shift, car.CRCtrlTime)
            headLight, HLCtrlTime = adapter.headLightState(car.headLight, car.HLCtrlTime)
            quitCtrl = adapter.quitState()

            if wii.getButtonState() - WII.BTN_RIGHT == 0 :
                raise util.ModeException
            
    except util.ModeException :
        autoMode, modeCtrlTime = util.changeMode(autoMode, modeCtrlTime)
        continue

    car.setShift(shift)
    car.setCruise(cruise, CRCtrlTime)
    car.setSpeed(speed)
    car.setSteer(steer)
    car.setHeadLight(headLight, HLCtrlTime)
    car.setQuitCtrl(quitCtrl)
    
    try :
        car.drive()
    except util.QuitException :
        del(car)
        cv2.destroyAllWindows()
        break
    
    sleep(DRIVE_DELAY)

print('RC Power OFF')
