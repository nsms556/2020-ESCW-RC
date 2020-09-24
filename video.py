from __future__ import division

import os, sys
import time, datetime
import argparse

import cv2
import matplotlib.pyplot as plt

import torch
from torch.autograd import Variable

from models import *
from utils.utils import *
from utils.datasets import *

CUDA = torch.cuda.is_available()
deviceNo =  'cuda:0' if CUDA else 'cpu'
Tensor = torch.cuda.FloatTensor if CUDA else torch.FloatTensor
device = torch.device(deviceNo)

SHOWIMAGE = False

VideoWidth = 960
VideoHeight = 540

cmap = plt.get_cmap('tab20b')
colors = [cmap(i) for i in np.linspace(0, 1, 20)]

def printInfo() :
    print('Torch Version : {0}'.format(torch.__version__))
    if CUDA :
        print('Tensor Device : {0}'.format(torch.cuda.get_device_name(deviceNo)))
    print('OpenCV Version : {0}'.format(cv2.__version__))

def cvImg_to_Tensor(img, inputDim) :
    img = cv2.resize(img, (inputDim, inputDim))
    img = img[:,:,::-1].transpose((2,0,1)).copy()
    img = torch.from_numpy(img).float().div(255.0).unsqueeze(0)

    return img

def detectVideo(model, opt, classes, frame) :
    detectList = []
    prevTime = time.time()
    
    #Convert to Tensor
    frameImg = frame.copy()
    frameDim = frameImg.shape[1], frameImg.shape[0]
    frameDim = torch.FloatTensor(frameDim).repeat(1,2).type(Tensor)
    frameTensor = cvImg_to_Tensor(frameImg, opt.img_size).type(Tensor)
    #print('Convert : {0}'.format(time.time() - prevTime))

    #Run Detection in frameImg
    with torch.no_grad() :
        detections = model(frameTensor).type(Tensor)
        #print('detect : {0}'.format(time.time() - prevTime))
        detections = write_results(detections, opt.conf_thres, len(classes), opt.nms_thres)
        #print('NMS : {0}'.format(time.time() - prevTime))

    # if Detection Objects Count is Zero
    if type(detections) == int :
        #print('1 frame : {0}\n'.format(time.time() - prevTime))
        return frameImg, detectList

    # Detected Location Rescale
    detections = new_rescale_boxes(detections, opt.img_size, frameImg.shape[:2])

    # Objects label & color Setting
    uniqueLabels = detections[:, -1].cpu().unique()
    nClsPreds = len(uniqueLabels)
    bBoxColors = random.sample(colors, nClsPreds)
        
    # Draw Object in frameImg
    for _, x1, y1, x2, y2, conf, clsConf, clsPred in detections :
        color = bBoxColors[int(np.where(uniqueLabels == int(clsPred))[0])]    
        cv2.rectangle(frameImg, (x1, y1), (x2, y2), color=color, thickness=2)
        cv2.putText(frameImg,  classes[int(clsPred)], (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1)
        detectList.append(classes[int(clsPred)])

    #print('1 frame time : {0}\n'.format(time.time() - prevTime))
    return frameImg, detectList

def loadModel(opt) :
    model = Darknet(opt.model_def, img_size=opt.img_size).to(device)
    if opt.weights_path.endswith('.weights') :
        model.load_darknet_weights(opt.weights_path)
    else :
        model.load_state_dict(torch.load(opt.weights_path))
    model.eval()
    classes = load_classes(opt.class_path)

    return model, classes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_def", type=str, default="config/yolov3-custom-test_ver1.cfg", help="path to model definition file")
    parser.add_argument("--weights_path", type=str, default="weights/TSRver1.pth", help="path to weights file")
    parser.add_argument("--class_path", type=str, default="config/classes.names", help="path to class label file")
    parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
    parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
    parser.add_argument("--batch_size", type=int, default=1, help="size of the batches")
    parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
    parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
    parser.add_argument("--checkpoint_model", type=str, help="path to checkpoint model")
    parser.add_argument("--show_image", type=str, default=None, help='show detection images like Video')
    opt = parser.parse_args()
    print(opt)

    opt.show_image = 'y'
    if opt.show_image is not None :
        SHOWIMAGE = True

    printInfo()

    cam = cv2.VideoCapture(0, cv2.CAP_V4L)

    device = torch.device(deviceNo)

    model, classes = loadModel(opt)

    if cam.isOpened() :
        cam.set(3, VideoWidth)
        cam.set(4, VideoHeight)
    else :
        print('NoVideo')
        exit()

    while True :
        ret, frame = cam.read()

        frameImg, detectList = detectVideo(model, opt, classes, frame)

        if SHOWIMAGE :
            cv2.imshow('Detect', frameImg)
        
        print(detectList)

        if cv2.waitKey(1) & 0xFF == 27 :
            break

    cv2.destroyAllWindows()
    if CUDA :
        torch.cuda.empty_cache()
        
