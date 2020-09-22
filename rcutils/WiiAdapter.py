from time import time 

import cwiid as WII

from rcutils.RCStatic import *

class WiiAdapter :
    def __init__(self, wii) :
        self.wii = wii

    def shiftState(self) :
        buttons = self.wii.getButtonState()

        if buttons & WII.BTN_2 and buttons & WII.BTN_1 :
            shift = SHIFT_STOP
        elif buttons & WII.BTN_2 == 0 and buttons & WII.BTN_1 == 0 :
            shift = SHIFT_STOP
        elif buttons & WII.BTN_2 :
            shift = SHIFT_FORWARD
        elif buttons & WII.BTN_1 :
            shift = SHIFT_BACKWARD

        return shift
    
    def steerValue(self) :
        steer = self.wii.getAccState()[1]

        if steer >= STEER_LEFTLIMIT :
            steer = STEER_LEFTLIMIT
        elif steer <= STEER_RIGHTLIMIT :
            steer = STEER_RIGHTLIMIT
        
        return steer
    
    def speedValue(self, speed, shift, cruise) :
        # DEFAULT
        '''
        if cruise == CRUISE_ON :
            newSpeed = speed
        elif shift == SHIFT_FORWARD or shift == SHIFT_BACKWARD :
            if speed + 0.2 <= SPEED_LIMIT :
                newSpeed = speed + 0.2
            else :
                newSpeed = speed
        else :
            if speed - 1 < 0 :
                newSpeed = 0
            else :
                newSpeed = speed - 1
        '''

        # Cannot PWM
        newSpeed = SPEED_LIMIT

        return newSpeed
        
    def headLightState(self, state, lastCtrlTime) :
        buttons = self.wii.getButtonState()

        light = state
        ctrlTime = lastCtrlTime

        if buttons & WII.BTN_DOWN :
            if time() - lastCtrlTime > CONTROL_IGNORE :
                light ^= True
                ctrlTime = time()

        return light, ctrlTime

    def cruiseState(self, state, speed, shift, lastCtrlTime) :
        buttons = self.wii.getButtonState()

        cruise = state
        ctrlTime = lastCtrlTime

        if buttons & WII.BTN_UP :
            if time() - lastCtrlTime > CONTROL_IGNORE and speed > CRUISE_MINIMUM :
                cruise ^= True
                ctrlTime = time()
        elif buttons & WII.BTN_1 :
            cruise = CRUISE_OFF
            ctrlTime = time()

        return cruise, ctrlTime    

    def quitState(self) :
        buttons = self.wii.getButtonState()

        if buttons - WII.BTN_PLUS - WII.BTN_MINUS == 0 :
            quitState = 1
        else :
            quitState = 0

        return quitState
