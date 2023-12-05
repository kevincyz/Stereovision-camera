import picamera
from picamera import PiCamera
import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
from time import sleep

#functions
import hsv_filter as hsv
import shape_recognition as shape
import triangulation as tri
import size as size

# Camera settimgs
cam_width = 1280
cam_height = 480

# Final image capture settings
scale_ratio = 0.5

# Camera resolution height must be dividable by 16, and width by 32
cam_width = int((cam_width+31)/32)*32
cam_height = int((cam_height+15)/16)*16

# Buffer for captured image settings
img_width = int (cam_width * scale_ratio)
img_height = int (cam_height * scale_ratio)
capture = np.zeros((img_height, img_width, 4), dtype=np.uint8)

# Initialize the camera
camera = PiCamera(stereo_mode='side-by-side',stereo_decimate=False)
#camera.resolution=(cam_width, cam_height)
camera.framerate = 20

B = 6.5 #distance between cameras in centimeters
f = 3.15 #focal length of the camera in millimeters
alpha = 160  #horizontal angle the camera can observe

#initial values
count = -1

for frame in camera.capture_continuous(capture, format="bgra", use_video_port=True, resize=(img_width,img_height)):
    frame_left = frame [0:img_height,0:int(img_width/2)] #Y+H and X+W
    frame_right = frame [0:img_height,int(img_width/2):int(img_width)] #Y+H and X+W
    count +=1
    depth = 0
    actual_width = 0
    
    if len(frame_left) == 0 or len(frame_right) == 0:
        break
    else:
        mask_right = hsv.add_HSV_filter(frame_right)
        mask_left = hsv.add_HSV_filter(frame_left)
        #result frames after applying the hsv filter
        res_right = cv2.bitwise_and(frame_right,frame_right,mask=mask_right)
        res_left = cv2.bitwise_and(frame_left,frame_left,mask = mask_left)
        

        #applying shape recognition
        circles_right,width1 = shape.find_circles(frame_right,mask_right)
        circles_left,width2 = shape.find_circles(frame_left,mask_left)
        
        '''
        calculating ball depth
        '''
        a = np.array(circles_right)
        b = np.array(circles_left)
        #if no ball can be tracked 
        if a.all() == None or b.all() == None:#error right here
            cv2.putText(frame_right,"Tracking lost",(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            cv2.putText(frame_left,"Tracking lost",(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

        else:
            #function that determines the depth of object and the area of 
            depth= tri.find_depth(circles_right,circles_left,frame_right,frame_left,B,f,alpha)
            print(str(depth)+" cm away")
            
            #theoretical width in pixels at this distance of the 10cm diameter object
            #theoretical = depth * (-1.0061)+155.59
            #print(theoretical)
            width2.sort()
            if len(width2) > 1: 
                reference_size = width2[1]
                actual_size = width2[0]
                print(reference_size,actual_size)
                actual_width = 10/reference_size * actual_size
                print(actual_width)
            #print('The width of the object is '+str(actual_width)+' cm')
            else :
                print("1 object")
            
            
            """alternative solution
            target_size_pixels = width #this is only applicable when there is one target sphere in the frame
            reference_size = depth * (-1.0061)+155.59
            actual_size = 10/reference_size * target_size_pixels
            
            """
            
            cv2.putText(frame_right,"TRACKING",(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(124,252,0),2)
            cv2.putText(frame_left,"TRACKING",(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(124,252,0),2) 
            cv2.putText(frame_right,"Distance+ "+str(round(depth,3)),(200,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(124,252,0),2)
            cv2.putText(frame_left,"Distance+ "+str(round(depth,3)),(200,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(124,252,0),2)
            
            
        
            
            
        #show the frames
        cv2.imshow("frame_right",frame_right)
        cv2.imshow("frame left",frame_left)
        cv2.imshow("mask_right",mask_right)
        cv2.imshow("mask_left",mask_left)


        #hit q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap_right.release()
cap_left.release()

cv2.destroyAllWindows()




        




