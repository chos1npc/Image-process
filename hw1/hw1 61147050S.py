from ctypes.wintypes import WORD
from turtle import left, width
import cv2

import numpy as np

import tkinter as tk

from PIL import Image, ImageTk

from tkinter import LEFT, RIGHT, Y, Scrollbar, StringVar, IntVar, ttk


from tkinter.filedialog import askopenfilename



window = tk.Tk()

window.title('AIP61147050S')
#window.geometry('1300x1100')


def OpenFile():

    #這是圖片檔的路徑(可接受JPG,PPM,BMP檔)
    global RGB_img,BGR_img,img_new
    
    filename = askopenfilename(title="Select JPG/BMP/PPM file", filetypes=(("JPG files", "*.jpg"),("PPM files","*.ppm"),("BMP files","*.bmp")))
    '''
    #用cv2載入圖片，不使用imread，因為它不支援中文。

    RGB_img = cv2.imdecode(np.fromfile(filename,dtype=np.uint8), cv2.IMREAD_COLOR) # imdecode 會轉圖片成RGB

    #將cv2的BGR轉成RGB

    BGR_img = cv2.cvtColor(RGB_img, cv2.COLOR_BGR2RGB)

    #重新調整圖片大小

    BGR_img=cv2.resize(BGR_img,(450,450))

    #將img載入為PIL的格式。

    im = Image.fromarray(BGR_img)

    #將img載入到ImageTK中

    photo = ImageTk.PhotoImage(im)
    '''
    #pillow處理圖片
    im = Image.open(filename)
    (width,height) = im.size
    width_new =512
    height_new =512
    if width/height>=width_new/height_new:
        img_new = im.resize((width_new, int(height*width_new /width)))
    else:
        img_new = im.resize((int(width*height_new/height),height_new))
    
    im_PIL = ImageTk.PhotoImage(img_new)
   #設定labelimg為圖片作顯示

    imglabel.configure(image=im_PIL)

    imglabel.image = im_PIL

    

    

def transpose():
    '''
    img_rotate = cv2.rotate(BGR_img, cv2.ROTATE_180)
    #cv2.imshow('rotate', img_rotate)
    #將img載入為PIL的格式。

    im = Image.fromarray(img_rotate)

    #將img載入到ImageTK中

    img_rotate = ImageTk.PhotoImage(im)
    '''
    #用pillow 旋轉圖片
    img_rotate = img_new.rotate(180)
    
    #將img載入到ImageTK中

    img_rotate = ImageTk.PhotoImage(img_rotate)

    imglabel2.configure(image=img_rotate)

    imglabel2.image = img_rotate
    #cv2.waitKey(0)



btn1 = tk.Button(window, text='open', font= 12, width=15, height=3, command=OpenFile)
btn1.grid(row=0,column=0)

btn2=tk.Button(window,text="旋轉圖片",font=12, width=15, height=3,command=lambda:transpose())
btn2.grid(row=0,column=1)


imglabel = tk.Label(window, image="")
imglabel.grid(row=1,column=0)

imglabel2 = tk.Label(window, image="")
imglabel2.grid(row=1,column=1)


window.mainloop()