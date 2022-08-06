import tkinter 
import numpy as np
import cv2 as cv
import math
import pyautogui
from tkinter import *
from PIL import Image, ImageTk
import os

root = tkinter.Tk()
root.geometry("2000x1000")
root.title("Game Over")

img = PhotoImage(file ="C:\\Users\\berfin\\Desktop\\dino_game\\assets\\game_over.png")
label = Label(
    root,
    image=img
    )
label.place(x=0,y=0)

def gameAutomation():
   # Kamera açma
   capture = cv.VideoCapture(0, cv.CAP_DSHOW)
   
   while capture.isOpened():

    # Kameradan kareleri yakalama
        ret, frame = capture.read()
        frame = cv.flip(frame,1) # kamera ayna görüntüsü için

    # Karelerden el verilerini almak
        cv.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
        # kırpma işlemi
        crop = frame[100:300, 100:300] #yeni bir nesne yerine orjinal görüntü üzerinde bir görünüm oluşturur

    # Gauss bulanıklığı uygulamak
        blur = cv.GaussianBlur(crop, (3, 3), 0) #görüntüyü yumuşatmak 

    # Renk alanını RGB -> HSV'den değiştirmek
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)

    # Beyazın ten rengi olacağı ve geri kalanın siyah olduğu bir ikili görüntü oluşturmak
        mask = cv.inRange(hsv, np.array([2, 0, 0]), np.array([25, 255, 255])) 

    # Morfolojik dönüşüm için 
        kernel = np.ones((5, 5))

    # Arka plan gürültüsünü filtrelemek 
        dilation = cv.dilate(mask, kernel, iterations=1) #görüntünün ön planını genişletmeyi içerir ve ön planın beyaz olması önerilir
        erosion = cv.erode(dilation, kernel, iterations=1) #görüntünün ön planını aşındırmayı içerir ve ön planın beyaz olması önerilir

    # Gauss Bulanıklığı ve Eşiği 
        filtered = cv.GaussianBlur(erosion, (3, 3), 0) 
        ret, thresh = cv.threshold(filtered, 127, 255, 0) #127 den büyük tüm pikseller 0 olacak şekilde thresh de tutulur

    # Kontür bul
        contours, hierachy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #elde edilen kontur görünrüdeki beyaz alanların vektörel ifadesi

        try:
        # Maksimum alana sahip kontör bulmak
            contour = max(contours, key=lambda x: cv.contourArea(x))

        # Kontur etrafında sınırlayıcı dikdörtgen oluşturmak
            x, y, w, h = cv.boundingRect(contour) # kontur çerçeve noktaları hesaplamak
            cv.rectangle(crop, (x, y), (x + w, y + h), (0, 0, 255), 0) # kontur etrafına çerçeve çizmek

        # Dışbükey gövde bulma
            hull = cv.convexHull(contour)

        # Kontur çizme
            drawing = np.zeros(crop.shape, np.uint8)
            cv.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
            cv.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

        # Dışbükey gövde 
            hull = cv.convexHull(contour, returnPoints=False) # cismin çevresindeki yeşil çerçeve
            defects = cv.convexityDefects(contour, hull)
        
        # Başlangıç ve bitiş noktasından uzak noktanın açısını, yani tüm kusurlar için dışbükey noktaları (parmak uçları) bulmak için kosinüs kuralı
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

        # Koşul eşleşiyorsa SPACE tuşuna bas

            if count_defects >= 4:
                    pyautogui.press('space')
                    cv.putText(frame, "JUMP", (115, 80), cv.FONT_HERSHEY_SIMPLEX, 2, 2, 2)

    
        except:
            pass

        cv.imshow("Gesture", frame)

    # Kamerayı kapat(0 ile)
        if cv.waitKey(1) == ord('0'):
            break

   capture.release()
   cv.destroyAllWindows()
 
# Arayüz için  
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
