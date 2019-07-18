from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import os
import threading

def f1():
    os.system('CallerMain.py')

def f2():
    root = Tk()
    root.mainloop()

def run():
    Voip_Frame.destroy()
    t1 = threading.Thread(target=f1)
    t2 = threading.Thread(target=f2)
    t1.start()
    t2.start()




Voip_Frame = Tk()
Voip_Frame.title("GoSecure")
Voip_Frame.geometry('900x500')
Voip_Frame.configure(background = 'gray15')
head = Label(Voip_Frame, text= "Make Encrypted Calls!", font='Helvetica 18 bold', foreground= 'white' , background = 'gray15').place(x=300, y= 10)
logo=ImageTk.PhotoImage(Image.open("wall.JPG"))
logoLbl = Label(Voip_Frame, borderwidth= 0, highlightthickness = 0, image=logo).place(x=320, y=65)
call = Label(Voip_Frame, text= "Enter goSecure id to make a call", font='Helvetica 15', foreground= 'white' , background = 'gray15').place(x=260, y= 260)

ip= Entry(Voip_Frame,  width = 40)
ip.place(x=280, y= 320)


call = Button(Voip_Frame, width = 10, text = "Call", font = 'bold', command = run)
call.config(background = 'green')
call.place(x=270 , y = 380)

stop = Button(Voip_Frame, width = 10, text = "Stop", font = 'bold')
stop.config(background = 'red')
stop.place(x=450 , y = 380)


call = Label(Voip_Frame, text= "Your Call are End to End Encrypted", font='Helvetica 8', foreground= 'white' , background = 'gray15').place(x=320, y= 440)


Voip_Frame.mainloop()