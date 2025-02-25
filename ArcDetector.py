# DUNE_NP02_currentAnalysis
# Current spike detection in ProtoDUNE NP02 using the object detection AI which detect the light flashes,
# compare it with the current data and provide us with the exact time and length frame when the current spike is seen.
import cv2
import urllib.request
import json
import pandas as pd
import datetime
import time
import numpy as np
import subprocess
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# input the video file name to detect the arc
file_name = input("Enter the File Name: ")
video_file = open(file_name, "r")

# Threshold set to cutoff the pollution below 252
thresholds = 252
# import the video file form the system and look for the corresponding events
cap = cv2.VideoCapture(file_name)
# Subract the background from the video to detect object
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
# counting the number of frame detected in the video file
count =0
# counting the number of frame where the event is located
frame_count = 0
# Array to store individual frame
Event_frame = []
while True:
    # isolate the video into seperate frame
    ret, frame=cap.read()           
    #frame[frame<=thresholds]=0
    # mask the video file
    mask = object_detector.apply(frame)
    # mask the backgroubd to the color ratio of 255 for complete black color
    _, mask  = cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     #applying contour to an arc
    res = cv2.bitwise_and(frame,frame,mask=mask)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # detect for the flashes above 1000pixel
        if area>1000:
            print("Area of contour:", area)
            cv2.drawContours(frame, [cnt], -1, (0,255,0),2)
            if True:
                print("Contour Detected")
                cv2.imwrite("vid%d.jpg"%count, frame)
                count +=1
                #cv2.imshow("Frame2", frame)  
                Event_frame.append(frame)

    key = cv2.waitKey(5)
    if key =='27':
        break
    # show frame video
    cv2.imshow("Frame",frame)
    # show mask video
    cv2.imshow("Mask",mask)
    frame_count +=1
    #print(frame_count)

# loop to concat all the frame together to produce the video file
# frame concat together to produce the video
# -r frame rate/speed of video file
for frames in Event_frame:
    ffmpeg -r 6 -i frames%d.jpg -c:v libx264 -vf fps=25 -pix_fmt yuv420p concat_video.mp4
                                                                                                     
# following result destroy all windows
result = cv2.VideoWriter('maskedvideo.mp4', cv2.VideoWriter_fourcc(*'MJPG'),10, size)
cap.release()
out.write(mask)
cv2.destroyAllWindow()
