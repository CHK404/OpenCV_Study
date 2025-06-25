import cv2
import numpy as np
import tkinter
from PIL import Image, ImageTk

img = cv2.imread('500px-Lenna.png')
img_RGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_BW = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

if img is None:
    print('이미지를 찾을 수 없습니다. 파일이 있는지 확인해주세요.')
    exit()
    
drawing = False
ix, iy = -1, -1

def draw_line(event, x, y, flags, param):
    global ix, iy, drawing, img_BW
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(img_BW, (ix, iy), (x, y), (0, 0, 0), thickness=2)
            ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img_BW, (ix, iy), (x, y), (0, 0, 0), thickness=2)
                
def change():
    global img_BW
    cv2.namedWindow('Gray')
    cv2.setMouseCallback('Gray', draw_line)
    while True:
        cv2.imshow('Gray', img_BW)
        if cv2.getWindowProperty('Gray', cv2.WND_PROP_VISIBLE) < 1:
            break
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    
def Contour():
    img_Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_threshold = cv2.threshold(img_Gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(img_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_Gray, contours, -1, (0, 0, 0), 2)
    cv2.imshow('Contours', img_Gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

window=tkinter.Tk()
window.title("Lenna")

img_PIL=Image.fromarray(img_RGB)
img_TK= ImageTk.PhotoImage(image=img_PIL)

label = tkinter.Label(window, image=img_TK)
label.pack()

button = tkinter.Button(window, text="change", command=change)
button.pack()
button = tkinter.Button(window, text="contours", command=Contour)
button.pack()
window.mainloop()
    
cv2.waitKey(0)
cv2.destroyAllWindows()