import sys
import cv2
import numpy as np
import time
import imutils

def find_circles(frame,mask):
    contours = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#dont know what this is
    contours = imutils.grab_contours(contours)
    center = None
    width_pixels = []

    #only process if one contour is found
    for c in contours: 
        #find the largest contour in the image
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"],),int(M["m01"]/M["m00"]))
        
        #only process if the radius is greater than a value
        if radius > 10: 
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(frame,center,5,(0,0,0),-1)
            width_pixels.append(float("{:.2f}".format(radius)))


    return center,width_pixels



