import cv2
import numpy as np
import tkinter
from PIL import Image, ImageTk

#이미지 파일 경로
img_path = '500px-Lenna.png'

#이미지 읽기
img = cv2.imread(img_path)
img_RGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#변환 함수
def change():
    img_BW = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Lenna BW', img_BW)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def line():
    img_Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_threshold = cv2.threshold(img_Gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(img_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_Contours = img.copy()
    cv2.drawContours(img_Contours, contours, -1, (255, 255, 255), 2)
    cv2.imshow('Contours', img_Contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
#이미지가 읽혔는지 확인
#if img is None:
    #print('이미지를 불러올 수 없습니다.')
#else:
    #이미지 창에 출력
    #cv2.imshow('Lenna Image', img)

window=tkinter.Tk()
window.title("Lenna BW")

img_PIL=Image.fromarray(img_RGB)
img_TK= ImageTk.PhotoImage(image=img_PIL)

label = tkinter.Label(window, image=img_TK)
label.pack()

button = tkinter.Button(window, text="change", command=change)
button.pack()
button = tkinter.Button(window, text="contours", command=line)
button.pack()
window.mainloop()

#키 입력 대기    
cv2.waitKey(0)
cv2.destroyAllWindows()