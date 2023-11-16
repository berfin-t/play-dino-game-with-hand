import tkinter 
import numpy as np                                        
import cv2 as cv
import math
import pyautogui
from tkinter import *
import os

root = tkinter.Tk()
root.geometry("2000x1000")
root.title("Game Over")

img = PhotoImage(file = "assets/game_over.png")
label = Label(
    root,
    image=img
    )
label.place(x=0,y=0)

def gameAutomation():
   # Open camera
   capture = cv.VideoCapture(0, cv.CAP_DSHOW)
   
   while capture.isOpened():

    # Capture frames from camera
        ret, frame = capture.read()
        frame = cv.flip(frame,1) # for camera mirror image

    # Get hand data from frames
        cv.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
        # crop operation
        crop = frame[100:300, 100:300] # creates a view on the original image instead of a new object

    # Apply Gaussian blur
        blur = cv.GaussianBlur(crop, (3, 3), 0) # soften the image

    # Changing color space from RGB -> HSV
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    # Creating a binary image where white will be the skin color and the rest will be black# Beyazın ten rengi olacağı ve geri kalanın siyah olduğu bir ikili görüntü oluşturmak
        mask = cv.inRange(hsv, np.array([2, 0, 0]), np.array([25, 255, 255])) 

    # For morphological transformation
        kernel = np.ones((5, 5))

   # Filtering background noise 
        dilation = cv.dilate(mask, kernel, iterations=1) #involves expanding the foreground of the image and it is recommended that the foreground be white
        erosion = cv.erode(dilation, kernel, iterations=1) #involves eroding the foreground of the image and it is recommended that the foreground be white

    # Gaussian Blur and Threshold 
        filtered = cv.GaussianBlur(erosion, (3, 3), 0) 
        ret, thresh = cv.threshold(filtered, 127, 255, 0) #All pixels greater than 127 are kept in thresh to 0.

    # Find contours
        contours, hierachy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #vector expression of the white areas in the resulting contour image

        try:
        # Find top up with maximum space
            contour = max(contours, key=lambda x: cv.contourArea(x))

        # Create bounding rectangle around contour
            x, y, w, h = cv.boundingRect(contour) # calculate contour frame points
            cv.rectangle(crop, (x, y), (x + w, y + h), (0, 0, 255), 0) # draw a frame around the contour

        # Finding convex hull
            hull = cv.convexHull(contour)

        # contour drawing
            drawing = np.zeros(crop.shape, np.uint8)
            cv.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
            cv.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

        # Convex hull
            hull = cv.convexHull(contour, returnPoints=False) # green frame around the object
            defects = cv.convexityDefects(contour, hull)
        
        # Cosine rule to find the angle of the point far from the start and end point, i.e. convex points (fingertips) for all defects
            count_defects = 0

            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])

                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

                if angle <= 90:
                    count_defects += 1
                    cv.circle(crop, far, 1, [0, 0, 255], -1)

                cv.line(crop, start, end, [0, 255, 0], 2)

       # If the condition matches, press SPACE

            if count_defects >= 4:
                    pyautogui.press('space')
                    cv.putText(frame, "JUMP", (115, 80), cv.FONT_HERSHEY_SIMPLEX, 2, 2, 2)

    
        except:
            pass

        cv.imshow("Gesture", frame)

   # Turn off camera (with 0)
        if cv.waitKey(1) == ord('0'):
            break

   capture.release()
   cv.destroyAllWindows()
 
# for interface  
B1 = tkinter.Button(
    root, 
    text ="Dino Game",
    fg='#FFFFFF',
    relief=RAISED,
    font=('Arial Bold', 18),
    bg='#000000',
    height = 1, 
    width = 10,
    command = gameAutomation
    )
B1.place(x=1250, y=315)

B2 = tkinter.Button(
    root, 
    text ="Game 2",
    fg='#FFFFFF',
    relief=RAISED,
    font=('Arial Bold', 18),
    bg='#000000',
    height = 1, 
    width = 10,
    #command = gameAutomation
    )
B2.place(x=1250, y=435)

B3 = tkinter.Button(
    root, 
    text ="Game 3",
    fg='#FFFFFF',
    relief=RAISED,
    font=('Arial Bold', 18),
    bg='#000000',
    height = 1, 
    width = 10,
    #command = gameAutomation
    )
B3.place(x=1250, y=555)

B4 = tkinter.Button(
    root, 
    text ="Game 4",
    fg='#FFFFFF',
    relief=RAISED,
    font=('Arial Bold', 18),
    bg='#000000',
    height = 1, 
    width = 10,
    #command = gameAutomation
    )
B4.place(x=1250, y=675)

root.mainloop() 
