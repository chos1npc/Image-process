
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import LEFT, RIGHT, Y, Scrollbar, StringVar, IntVar, ttk
import random
import math
from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.title('AIP61147050S')
# root.geometry('500x500')

def OpenFile():
    global img_new
    #這是圖片檔的路徑(可接受JPG,PPM,BMP檔)
    
    
    filename = askopenfilename(title="Select JPG/BMP/PPM file", filetypes=(("JPG files", "*.jpg"),("PPM files","*.ppm"),("BMP files","*.bmp")))
    
    #pillow處理圖片
    im = Image.open(filename)
    (width,height) = im.size
    width_new =250
    height_new =250
    if width/height>=width_new/height_new:
        img_new = im.resize((width_new, int(height*width_new /width)))
    else:
        img_new = im.resize((int(width*height_new/height),height_new))
    
    im_PIL = ImageTk.PhotoImage(img_new)
   #設定labelimg為圖片作顯示

    # imglabel.configure(image=im_PIL)

    # imglabel.image = im_PIL
    label1.configure(image = im_PIL)
    label1.image = im_PIL
    label1.pack()

def transpose():
    #用pillow 旋轉圖片
    img_rotate = img_new.rotate(180)
    #將img載入到ImageTK中
    img_rotate = ImageTk.PhotoImage(img_rotate)
    label2.configure(image=img_rotate)
    label2.image = img_rotate
    label2.pack()

def Hist(im, x, y):
    
    f = Figure(figsize = (4, 3))
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.get_tk_widget().grid(row=x, column=y, padx = 12, pady = 15)
    
    p = f.gca()
    p.hist(np.ravel(im.convert('L')), 256, [0, 256], density=True)

def hist_grayimage():
    
    Hist(img_new, 2, 0)




def resize(im,new_size):
    w, h= im.size
    if w / h >= 1:
        im_newsize = im.resize((new_size, int(h * new_size / w)))
    else:
        im_newsize = im.resize((int(w * new_size / h), new_size ))
        
    return im_newsize

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
    # im = Image.new(mode = "L", size = (320, 320))
    # img_nos.show()

    conv = ImageTk.PhotoImage(image = img_nos)
    label2.configure(image = conv)
    label2.image = conv
    label2.pack()

    conv_pix = ImageTk.PhotoImage(image = img_conv)
    label3.configure(image = conv_pix)
    label3.image = conv_pix
    label3.pack()

    Hist(img_new, 2, 0)
    Hist(img_nos, 2, 2)
    Hist(img_conv, 2, 1)


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
    label3.configure(image=img_spnew)
    label3.image = img_spnew
    label3.pack()

    spnoise = Image.fromarray(grayimg)
    img_sppix = ImageTk.PhotoImage(image = spnoise)
    label2.configure(image=img_sppix)
    label2.image = img_sppix
    label2.pack()

    Hist(img_new,2,0)
    Hist(spnoise,2,1)
    Hist(img_sp,2,2)

def conv(mask,img_new):

    gray = img_new.convert('L')
    input = np.asarray(gray)
    n,m = input.shape
    
    img = []
    for i in range(n-5):
        line = []
        for j in range(m-5):
            a = input[i:i+5,j:j+5]
            line.append(np.sum(np.multiply(mask, a)))
        img.append(line)
    img = np.array(img)
    # new = Image.fromarray(img)
    conv_show = Image.fromarray(img)
    img_conv = ImageTk.PhotoImage(image = conv_show)
    label2.configure(image=img_conv)
    label2.image = img_conv
    label2.pack()
def historam_equalize():

    input = img_new.convert('L')
    w,h = input.size
    px = np.array(input)

    px_hist = np.histogram(px,bins= 256)[0]
    cu_hist = [px_hist[0]]
    constant = 255/w/h
    tp_list = np.zeros(256)
    for i in range(1,256):
        temp = px_hist[i]+cu_hist[i-1]
        cu_hist.append(temp)
        tp = round(cu_hist[i]*constant)
        tp_list[i] = tp
    # for i in range(1,256):
    #     px[px==(256-i)] = tp_list[256-i]
    for i in range(0,w-1):
        for j in range(0,h-1):
            g = px[j,i]
            px[j,i] = tp_list[g]

    px_img = Image.fromarray(px)
    equalize = ImageTk.PhotoImage(image = px_img)
    label2.configure(image = equalize)
    label2.image = equalize
    label2.pack()
    hist_grayimage()
    Hist(px_img,2,1)
    





def callbackFunc(event):
    global window
    if img_new == 0:
        textlabel.configure(text='PLEASE SELECT AN IMAGE')
        textlabel.pack(side=tk.LEFT)
    else:
    
        if list0.current() == 2:
            dobtn.configure(command = transpose)
            dobtn.pack()

        elif list0.current() == 3:
            dobtn.configure(command = hist_grayimage)
            dobtn.pack()

        elif list0.current() == 4:
            dobtn.configure(command = lambda : salt_pepper(spinbox.get()))
            dobtn.pack()

            spinbox.configure(from_ = 0, to = 100, width = 10)
            spinbox.pack(side=tk.RIGHT)

            textlabel.configure(text='PERCENTAGE : ')
            textlabel.pack(side=tk.LEFT)

        elif list0.current() == 5:
            dobtn.configure(command = lambda : Gaussian_noise(spinbox.get()))
            dobtn.pack()

            spinbox.configure(from_ = 0, to = 1000, width = 10)
            spinbox.pack(side=tk.RIGHT)

            textlabel.configure(text='VARIANCE : ')
            textlabel.pack(side=tk.LEFT)

        elif list0.current() ==6:
            
            dobtn.configure(command = get_entry)
            
            dobtn.pack()
        elif list0.current() ==7:
            
            dobtn.configure(command = historam_equalize)
            
            dobtn.pack()

def get_entry():
    global all_entries,demand
    window = tk.Toplevel(root)
    window.title('請輸入5*5矩陣')
    rows = 5
    cols = 5
    demand = np.zeros((rows, cols))
    all_entries = []
    for r in range(rows):
        entries_row = []
        for c in range(cols):
            e = tk.Entry(window, width=5)  # 5 chars
            e.insert('end', 0)
            e.grid(row=r, column=c)
            entries_row.append(e)
        all_entries.append(entries_row)

    b = tk.Button(window, text='get conv', command=get_data)
    b.grid(row=5,column=2)       

def get_data():
    for r, row in enumerate(all_entries):
        for c, entry in enumerate(row):
            text = entry.get()
            demand[r,c] = float(text)
    conv(demand,img_new)
    # return demand

group0 = tk.LabelFrame(root, text='openfile', padx=10, pady=10)
group0.grid( row=0, column=0, ipadx=12, ipady=12)
group1 = tk.LabelFrame(root, text='select', padx=10, pady=10)
group1.grid( row=0, column=1, ipadx=12, ipady=12)
group2 = tk.LabelFrame(root, text='openfile', padx=10, pady=10)
group2.grid( row=0, column=2, ipadx=12, ipady=12)
group3 = tk.LabelFrame(root, text='', padx=10, pady=10)
group3.grid( row=0, column=3, ipadx=12, ipady=12)

group10 = tk.LabelFrame(root, padx=12, pady=12, bd = 0)
group10.grid( row=1, column=0, ipadx=12, ipady=12)
group11 = tk.LabelFrame(root, padx=12, pady=12, bd = 0)
group11.grid( row=1, column=1, ipadx=12, ipady=12)
group12 = tk.LabelFrame(root, padx=12, pady=12, bd = 0)
group12.grid( row=1, column=2, ipadx=12, ipady=12)
group20 =tk.LabelFrame(root, padx=12, pady=12, bd = 0)
group20.grid( row=2, column=0, ipadx=12, ipady=12)
group21 = tk.LabelFrame(root, padx=12, pady=12, bd = 0)
group21.grid( row=2, column=1, ipadx=12, ipady=12)
group22 = tk.LabelFrame(root, padx=10, pady=10, bd = 0)
group22.grid( row=2, column=2, ipadx=12, ipady=12)

label1 = tk.Label(group10, image = "")
label2 = tk.Label(group11, image = "")
label3 = tk.Label(group12, image = "")
openbtn = tk.Button(group0, text='open', width = 10, height = 1, padx = 12, pady = 15, command = OpenFile)
openbtn.pack()
dobtn = tk.Button(group3, text='執行', width = 10, height = 1, padx = 12, pady = 15)
list0 = ttk.Combobox(group1, values=["", "choose one", "rotate", "hist", "pepper_and_salt", "gaussian", "convlution","historam_equalize`"])
list0.pack()
list0.current(1)
spinbox=ttk.Spinbox(group2)
textlabel = tk.Label(group2)
list0.bind("<<ComboboxSelected>>", callbackFunc)
root.mainloop()