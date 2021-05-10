# AirMouse Concept is developed from Scratch by Raja Ragavan.
# follow me in Facebook Instagram linkedIn
# RustyPrione

import cv2
import numpy as np
import handtrackingmodule as htm
import time
import autopy

######################
# Initializing Global variables
width_of_the_cam, height_of_the_cam=640,480
frameReduction=100    #frame Reduction
smoothening = 7       # To Reduce mouse shaking mechanism
######################

# For FPS
previousTime = 0
currentTime = 0

# For Mouse Location
previous_location_X,previous_location_Y=0,0
current_location_X,current_location_Y=0,0

# CV2 Initialization
capture=cv2.VideoCapture(0)
capture.set(3, width_of_the_cam)
capture.set(4, height_of_the_cam)

# detecting hands
detector = htm.handDetector(maxHands=1)

# Getting your display screen size using autopy
width_of_the_Screen, height_of_the_Screen = autopy.screen.size()
#print(width_of_the_Screen, height_of_the_Screen)

while True:
    success, img=capture.read()
    img=detector.findHands(img)
    landmarklist ,boundarybox=detector.findPosition(img) # Getting hand landmarks and setting boundary box for hand.

    if len(landmarklist)!=0:
        x1, y1 = landmarklist[8][1:]
        x2, y2 = landmarklist[12][1:]

        # print(x1,y1,x2,y2)         <-- tested for getting landmarks
        # Detecting finger up for mouse movement
        # Info : If Fingers are up then it returns 1 and if Fingers are down returns O

        fingers = detector.fingersUp()

        # print(fingers) <-- tested for getting fingers up are not
        cv2.rectangle(img, (frameReduction, frameReduction), (width_of_the_cam - frameReduction, height_of_the_cam - frameReduction), (255, 0, 255), 2)

        # Info :
        # fingers[0] is Thumb
        # fingers[1] is Index Finger
        # fingers[2] is Middle Finger
        # fingers[3] is Ring Finger
        # fingers[4] is last Finger
        # Info : If Fingers are up then it returns 1 and if Fingers are down returns O

        #Checking if Index finger is up or not for mouse movement
        if fingers[1]==1 and fingers[2]==0:

            # using Numpy Functions
            x3 = np.interp(x1, (frameReduction,width_of_the_cam - frameReduction),(0,width_of_the_Screen))
            y3 = np.interp(y1, (frameReduction, height_of_the_cam - frameReduction), (0, height_of_the_Screen))

            # for reducing mouse shakiness
            current_location_X=previous_location_X+(x3-previous_location_X)/smoothening
            current_location_Y = previous_location_Y+(y3 - previous_location_Y)/smoothening

            # mouse move operation using autopy
            autopy.mouse.move(width_of_the_Screen-current_location_X,current_location_Y)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            previous_location_X,previous_location_Y=current_location_X,current_location_Y  #Updating mouse loactions

        # Info :
        # fingers[0] is Thumb
        # fingers[1] is Index Finger
        # fingers[2] is Middle Finger
        # fingers[3] is Ring Finger
        # fingers[4] is last Finger
        # Info : If Fingers are up then it returns 1 and if Fingers are down returns O

        # Checking if Index finger and middle finger is up to enable Clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo =detector.findDistance(8,12,img)
            print(length)

            # Check if the distance between index and middle finger is below 30 then enable mouse click
            if length<20:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 255), cv2.FILLED)
                autopy.mouse.click()

    # To calculate FPS
    currentTime = time.time()
    FramesPerSecond = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv2.putText(img, str(int(FramesPerSecond)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Listening AirMouse via camera
    cv2.imshow("AirMouse - Raja Ragavan (RUSTYPRIONE,Inc.)", img)
    cv2.waitKey(1)