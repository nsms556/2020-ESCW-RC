from time import time
import cv2, argparse

import cwiid as WII

from LaneDetect_CV2 import laneDetectCV2
from rcutils.RCStatic import *
import video

parser = argparse.ArgumentParser()
parser.add_argument("--model_def", type=str, default="config/TSRver2.cfg", help="path to model definition file")
parser.add_argument("--weights_path", type=str, default="weights/TSRver2.pth", help="path to weights file")
parser.add_argument("--class_path", type=str, default="config/classes.names", help="path to class label file")
parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
parser.add_argument("--batch_size", type=int, default=1, help="size of the batches")
parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
parser.add_argument("--checkpoint_model", type=str, help="path to checkpoint model")
parser.add_argument("--show_image", type=str, default=None, help='show detection images like Video')
opt = parser.parse_args()

class AIController :
    def __init__(self, cam, wii) :
        self.TSRmodel, self.TSRclass = video.loadModel(opt)
        self.cam = cam
        self.wii = wii
        self.laneDetect = laneDetectCV2()
    
    def shiftState(self, state) :
        buttons = self.wii.getButtonState()

        if buttons & WII.BTN_2 :
            newState = SHIFT_FORWARD
        else :
            newState = SHIFT_STOP

        return newState
    
    def steerValue(self, show=False) :
        _, frame = self.cam.read()

        steer, processedImage = self.laneDetect.follow_lane(frame)

        if show :
            cv2.imshow('steer', processedImage)
            cv2.waitKey(1)

        steer = convertSteer(steer)
        
        if steer >= STEER_LEFTLIMIT :
            steer = STEER_LEFTLIMIT
        elif steer <= STEER_RIGHTLIMIT :
            steer = STEER_RIGHTLIMIT
  
        return steer

    def speedValue(self, speed) :
        newSpeed = speed

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

    def runTSR(self, show = False) :
        ret, frame = self.cam.read()

        TSRimage, TSRlist = video.detectVideo(self.TSRmodel, opt, self.TSRclass, frame)

        if show :
            cv2.imshow('TSR', TSRimage)
            cv2.waitKey(1)

        return TSRlist

    def headLightState(self, sensorValue) :
        # Need Illumi Sensor
        if sensorValue < HEADLIGHT_THRESHOLD :
            light = True
        else :
            light = False

        light = False

        return light, time()

def convertSteer(value) :
    return int(195 - (value / 6 * 5))

if __name__ == "__main__" :
    print(opt) 

    cam = cv2.VideoCapture(0, cv2.CAP_V4L)

    if cam.isOpened() :
        cam.set(3, 640)
        cam.set(4, 360)
    else :
        print('NoVideo')
        exit()
    
    test = AIController(cam, None)

    while True :
        _, frame = cam.read()

        steer = test.steerValue(True)
        tsr = test.runTSR(True)

        print(steer)
        print(tsr)

        if cv2.waitKey(1) & 0xFF == 27 :
            break

    cv2.destroyAllWindows()
    cam.release()
    if video.CUDA :
        torch.cuda.empty_cache()
        


   

