import sys
import cv2
import numpy as np
import time

def find_depth(circle_right,circle_left,frame_right,frame_left,baseLine,f,alpha):
    #convert focal length from mm to pixels
    height_right,width_right,depth_right = frame_right.shape
    height_left,width_left,depth_left = frame_left.shape
        

    if width_right == width_left:
        global f_pixel
        f_pixel =  (width_right*0.5)/np.tan(alpha*0.5*np.pi/180)
    
    
    else:
        print('Left and right do not have the same pixel width')


    x_right = circle_right[0]
    x_left = circle_left[0]

    #calculate the disparity
    disparity = x_right-x_left        #displacement between left and right frames [pixels]
    #calculate depth z
    zDepth= (baseLine*f_pixel)/disparity  #depth list in cm


    return abs(zDepth)

