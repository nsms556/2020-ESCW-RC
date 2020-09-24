from time import time

import cv2

from rcutils.RCStatic import CONTROL_IGNORE

def waveTimeToDis(time) :
    return time / 58.0

def steerValueToSig(value) :
    if value >= 117 and value <= 123 :
        signal = 7.7
    else :
        signal = round((float(200 - value) / 10), 1)
        if signal <= 5 :
            signal = 5
        elif signal >= 10.5 :
            signal = 10.5

    return signal

class QuitException(Exception) :
    pass

class ModeException(Exception) :
    pass

def changeMode(nowMode, lastCtrlTime) :
    newMode = nowMode
    ctrlTime = lastCtrlTime

    if time() - ctrlTime > CONTROL_IGNORE :
        newMode = nowMode ^ True
        ctrlTime = time()

    print('Driving Assist Mode : {}'.format(newMode))

    return newMode, ctrlTime

def cameraOpen() :
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)

    if camera.isOpened() :
        camera.set(3, 960)
        camera.set(4, 540)
    else :
        print('NoVideo')
        exit()
    
    return camera