from ctypes.wintypes import WORD
from turtle import left, width

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import tkinter as tk

from PIL import Image, ImageTk

from tkinter import LEFT, RIGHT, Y, Scrollbar, StringVar, IntVar, ttk

import random
import math
from tkinter.filedialog import askopenfilename

from pyparsing import col



window = tk.Tk()

window.title('AIP61147050S')
#window.geometry('1300x1100')


def OpenFile():

    #這是圖片檔的路徑(可接受JPG,PPM,BMP檔)
    global RGB_img,BGR_img,img_new,im
    
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
    width_new =320
    height_new =320
    if width/height>=width_new/height_new:
        img_new = im.resize((width_new, int(height*width_new /width)))
    else:
        img_new = im.resize((int(width*height_new/height),height_new))
    
    im_PIL = ImageTk.PhotoImage(img_new)
   #設定labelimg為圖片作顯示

    imglabel.configure(image=im_PIL)

    imglabel.image = im_PIL
    imglabel.grid(row=1,column=0)

    

    

    

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
    imglabel2.grid(row=1,column=1)

    #cv2.waitKey(0)

def hist():
    # 畫出直方圖
    plt.hist(np.ravel(im,order='C'), 256, [0, 255], density=True)
    plt.savefig('hist.png')

    gray = Image.open("hist.png")
    #pillow處理圖片
    # gray = Image.open("hist.png")
    (width,height) = gray.size
    width_new =320
    height_new =320
    if width/height>=width_new/height_new:
        img_new = gray.resize((width_new, int(height*width_new /width)))
    else:
        img_new = gray.resize((int(width*height_new/height),height_new))
    
   #設定labelimg為圖片作顯示

    # imglabel.configure(image=im_PIL)

    # imglabel.image = im_PIL
    gray_new = ImageTk.PhotoImage(image = img_new)
    imglabel3.configure(image = gray_new)
    imglabel3.image = gray_new
    imglabel3.grid(row=2,column=0)

    


def Gaussian_noise(Var):
    global img_conv,img_new
    global img_nos
    img_conv = img_new.convert('L')
    img_nos = img_new.convert('L')
    # print(img_conv)
    (width,height) = img_conv.size
    for h in range(0,height,2):
        for w in range(0,width):
            pixels=img_conv.load()
            pixel_nos=img_nos.load()
            pixel1= pixels[w,h]
            pixel2 =pixels[w,h+1]
            

            r = random.random()
            x = random.random()
            pi = math.pi
            cos = math.cos(2*pi*x)
            sin = math.sin(2*pi*x)
            ln = np.log(r)
            
            sqrt = math.sqrt((-2)*ln*r)
            z1 = int(Var)*cos*sqrt
            
            z2 = int(Var)*sin*sqrt
            pixel1 = pixel1+z1
            pixel2 = pixel2+z2

            if z1 <0:
                pixel_nos[w,h] = 0
            elif z1>255:
                pixel_nos[w,h] = 255
            else:
                pixel_nos[w,h] = int(z1)
            if z2 <0:
                pixel_nos[w,h+1] = 0
            elif z2 >255:
                pixel_nos[w,h+1] = 255
            else:
                pixel_nos[w,h+1] = int(z2)
            

                
            if pixel1 <0:
                pixels[w,h] = 0
            elif pixel1>255:
                pixels[w,h] = 255
            else:
                pixels[w,h] = int(pixel1)
            if pixel2 <0:
                pixels[w,h+1] = 0
            elif pixel2>255:
                pixels[w,h+1] = 255
            else:
                pixels[w,h+1] = int(pixel2)
    # print(f"{Var} 完成")
    im = Image.new(mode = "L", size = (320, 320))
    # img_nos.show()

    conv = ImageTk.PhotoImage(image = img_nos)
    labelnos_gau.configure(image = conv)
    labelnos_gau.image = conv
    labelnos_gau.grid(row=1,column=1)

    conv_pix = ImageTk.PhotoImage(image = img_conv)
    labelconv_gau.configure(image = conv_pix)
    labelconv_gau.image = conv_pix
    labelconv_gau.grid(row =1,column=2)

    plt.hist(np.ravel(im,order='C'), 256, [0, 255], density=True)
    plt.savefig('hist.png')
    gray = Image.open("hist.png")
    plt.hist(np.ravel(img_nos,order='C'), 256, [0, 255], density=True)
    plt.savefig('gaussian_nos.png')
    gaunoi = Image.open("gaussian_nos.png")
    # plt.close()
    plt.hist(np.ravel(img_conv,order='C'), 256, [0, 255], density=True)
    plt.savefig('gaussian_img.png')
    gaunoiimg = Image.open("gaussian_img.png")
    # plt.close()
    (width,height) = gaunoi.size
    (width,height) = gaunoiimg.size
    (width,height) = gray.size
    width_new =320
    height_new =320
    if width/height>=width_new/height_new:
        gaunoi = gaunoi.resize((width_new, int(height*width_new /width)))
        gaunoiimg = gaunoiimg.resize((width_new, int(height*width_new /width)))
        img_new = gray.resize((width_new, int(height*width_new /width)))
    else:
        gaunoi = gaunoi.resize((int(width*height_new/height),height_new))
        gaunoiimg = gaunoiimg.resize((int(width*height_new/height),height_new))
        img_new = gray.resize((int(width*height_new/height),height_new))

    img_gray = ImageTk.PhotoImage(image = img_new)
    imglabel0.configure(image = img_gray)
    imglabel0.image = img_gray
    imglabel0.grid(row=2,column=0)

    gaunoi_img = ImageTk.PhotoImage(image = gaunoi)
    imglabelgaunoi.configure(image = gaunoi_img)
    imglabelgaunoi.image = gaunoi_img
    imglabelgaunoi.grid(row=2,column=1)

    gaunoi_img_new = ImageTk.PhotoImage(image = gaunoiimg)
    labelgaunoi.configure(image = gaunoi_img_new)
    labelgaunoi.image = gaunoi_img_new
    labelgaunoi.grid(row=2,column=2)



def salt_pepper(rrate):
    global img_new
    rate=np.float32(rrate)/100
    # rate = 0.1
    half_rate = rate/2
    img_sp = img_new.convert('L')
    # print(img_sp)
    w,h = img_sp.size
    grayimg = np.zeros((w,h),np.float32)
    grayimg[:,:] = 128
    # print(grayimg)
    for k in range(0,w):
        for l in range(0,h):
            i =k,l
            # print(i)
            rdn = random.uniform(0,1)
            if rdn<half_rate:
                img_sp.putpixel(i,0)
                grayimg[k][l]=0

            elif rdn>1-half_rate:
                img_sp.putpixel(i,255)
                grayimg[k][l]=255
    # print(grayimg)
    # res_image = Image.fromarray(res)
    img_spnew = ImageTk.PhotoImage(image = img_sp)
    imglabelsp.configure(image=img_spnew)
    imglabelsp.image = img_spnew
    imglabelsp.grid(row =1,column=2)

    spnoise = Image.fromarray(grayimg)
    img_sppix = ImageTk.PhotoImage(image = spnoise)
    imglabelsppix.configure(image=img_sppix)
    imglabelsppix.image = img_sppix
    imglabelsppix.grid(row =1,column=1)



    
    plt.hist(np.ravel(im,order='C'), 256, [0, 255], density=True)
    plt.savefig('hist.png')
    gray = Image.open("hist.png")
    plt.hist(np.ravel(img_sp,order='C'), 256, [0, 255], density=True)
    plt.savefig('sp_nos.png')
    sp_nos = Image.open("sp_nos.png")
    # plt.close()
    plt.hist(np.ravel(spnoise,order='C'), 256, [0, 255], density=True)
    plt.savefig('sp_img.png')
    imagesp = Image.open("sp_img.png")
    # plt.close()
    (width,height) = sp_nos.size
    (width,height) = imagesp.size
    (width,height) = gray.size
    width_new =320
    height_new =320
    if width/height>=width_new/height_new:
        sp_nos = sp_nos.resize((width_new, int(height*width_new /width)))
        imagesp = imagesp.resize((width_new, int(height*width_new /width)))
        img_new = gray.resize((width_new, int(height*width_new /width)))
    else:
        sp_nos = sp_nos.resize((int(width*height_new/height),height_new))
        imagesp = imagesp.resize((int(width*height_new/height),height_new))
        img_new = gray.resize((int(width*height_new/height),height_new))

    img_gray = ImageTk.PhotoImage(image = img_new)
    imglabel0.configure(image = img_gray)
    imglabel0.image = img_gray
    imglabel0.grid(row=2,column=0)

    sp_img = ImageTk.PhotoImage(image = sp_nos)
    labelsp.configure(image = sp_img)
    labelsp.image = sp_img
    labelsp.grid(row=2,column=1)

    sp_img_new = ImageTk.PhotoImage(image = imagesp)
    labelsp_new.configure(image = sp_img_new)
    labelsp_new.image = sp_img_new
    labelsp_new.grid(row=2,column=2)



# entry of gaussianVar
Var = tk.StringVar()
# mylabel = tk.Label(window, text='Var:')
# mylabel.grid(row=0, column=3)
myentry = tk.Entry(window,textvariable=Var)
myentry.grid(row=0, column=3)

# entry of salt and pepper
sp = tk.StringVar()
# mylabel = tk.Label(window, text='sp:')
# mylabel.grid(row=0, column=3)
myentry = tk.Entry(window,textvariable=sp)
myentry.grid(row=0, column=6)

# button of openfile
btn1 = tk.Button(window, text='open', font= 8, width=8, height=1, command=OpenFile)
btn1.grid(row=0,column=0)

# button of transpose
btn2=tk.Button(window,text="旋轉圖片",font=8, width=8, height=1,command=lambda:transpose())
btn2.grid(row=0,column=1)
# button of hist
btn3=tk.Button(window,text="grayhist",font=8, width=8, height=1,command=lambda:hist())
btn3.grid(row=0,column=2)
# button of gaussian noise
btn4=tk.Button(window,text="Gaussian",font=8, width=8, height=1,command=lambda:Gaussian_noise(Var.get()))
btn4.grid(row=0,column=5)

# button of salt and pepper
btn5=tk.Button(window,text="salt and pepper",font=8, width=8, height=1,command=lambda:salt_pepper(sp.get()))
btn5.grid(row=0,column=7)
# label of original image
imglabel0 = tk.Label(window, image="")
imglabel = tk.Label(window, image="")
imglabel2 = tk.Label(window, image="")
imglabel3 = tk.Label(window, image="")
labelnos_gau =tk.Label(window, image="")
labelconv_gau =tk.Label(window, image="")
imglabelsp =tk.Label(window, image="")
imglabelsppix =tk.Label(window, image="")
imglabelgaunoi =tk.Label(window, image="")
labelgaunoi =tk.Label(window, image="")
labelsp = tk.Label(window, image="")
labelsp_new = tk.Label(window, image="")
window.mainloop()