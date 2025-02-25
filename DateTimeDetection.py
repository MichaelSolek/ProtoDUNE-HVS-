import cv2
import urllib.request
import json
import pandas as pd
import datetime
import time
import numpy as np
import subprocess
import pytesseract
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# FUNCTION takes the date and time from the file_name and convert it to the unix time format for the event current time synchronyzation 

file_name = input("Enter the File Name: ")
video_file = open(file_name, "r")
#file_name ='2021-12-06-20.43.50 maxCurrent 12.627 uA fromVideoStarting 20211206-20.40.00..mp4'       #To Decrease redundency to type file-name
video_file = open(file_name,"r")

#video_start_time(file_name)
thresholds = 252
# import the video file form the system and look for the corresponding events
cap = cv2.VideoCapture(file_name)
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  
print("frame dimentions: ", width, height )
# Extract the background
object_detector = cv2.createBackgroundSubtractorMOG2()
fps = cap.get(cv2.CAP_PROP_FPS) 
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(frame_count)
duration = frame_count/fps
print("Number of Frame: "+str(frame_count))
print('duration (S) = ' + str(duration))
minutes = int(duration/60)
seconds = duration%60
print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
count =0
frame_count = 0
date_data = []
while True:
    ret, frame=cap.read()
    if ret:
        #frame[frame<=thresholds]=0
        mask = object_detector.apply(frame)
        # mask the background to the color ration of 255 for complete black color
        _, mask  = cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
        contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        res = cv2.bitwise_and(frame,frame,mask=mask)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # detect flashes over 1000pixel
            if area>10000:
                #print("Area of contour:", area)
                #cv2.drawContours(frame, [cnt], -1, (0,255,0),2)
                x = int(0)
                y = int(0)
                w = int(1920)  
                h = int(1080)
                # Drawing a rectangle on copied image
                rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Cropping the text block for giving input to OCR
                cropped = frame[y:y + h, x:x + w]      
                ## Open the file in append mode
                #file = open("recognized.txt", "a")
                # Apply OCR on the cropped image
                text = pytesseract.image_to_string(cropped)
                print(text)
                date_data.append(text)   
    else:
        break    
    if cv2.waitKey(20) == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
