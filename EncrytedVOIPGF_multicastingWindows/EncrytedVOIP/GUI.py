from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import os
from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import threading
from database import database

from TCPSender import MicUDPCommunicator
from TCPReciver import SpeakerUDPCommunicator
from CallersProfile import PersonProfile
from ProcessBytes import ProcessBytes, PacketDetails, PersonProfile
from threading import Thread
from time import sleep
import math
from CallerMain import PhoneTerminal
from VideoGUI import VideoGUI




def GUI():
    Voip_Frame_key_page = Tk()
    frame = None

    status = Tkinter.StringVar()
    dial = Tkinter.StringVar()
    PT =None
    
    def putStatus(message):
         #global status
         status.set(message)

    def CreatePhoneTermianl():
        MicUDPCommunicator.printListOfMicDevices()
        SpeakerUDPCommunicator.printListOfSpeakerDevices()
        micDeviceID = -1
        outDeviceID = -1
        global PT
        PT = PhoneTerminal(micDeviceID, outDeviceID)
        PT.fnPrint = putStatus
        if(PT.enableVideoCalling):
            tw = Tkinter.Toplevel()
            frame = VideoGUI(master = tw, Width = 640, Height = 480, imageWidth = 640, imageHeight=480)
            frame.startCamera(PT.VideoReciver)
            frame.pack()
            tw.after(0,frame.Loop)
        sleep(2)

    def MakeCall():
        global PT
        if(PT.ConnectionStatus != 'ringing'):
           dt = database()
           dia =dt.getRecieverIP(dial.get())
           print("Here", dia)
           PT.ConnectTo(dia)
        else:
           PT.ConnectionStatus = 'pickup'

    def CloseCall():
        global PT
        PT.ConnectionStatus = "Disconnect"
    
    def EnterPhysicalKeyDetails():
        keyDetails = ip.get()
        ProcessBytes.UserProfile = PersonProfile(keyDetails)
        ip.delete(0, 'end')


    CreatePhoneTermianl()





    Voip_Frame_key_page.title("Encryptsy")
    Voip_Frame_key_page.geometry('500x600')
    Voip_Frame_key_page.configure(background='white')

    logo = ImageTk.PhotoImage(Image.open("logo1.png"))
    logoLbl = Label(Voip_Frame_key_page, borderwidth=0, highlightthickness=0, image=logo).place(x=215, y=30)

    logo_text = ImageTk.PhotoImage(Image.open("logo_text.png"))
    logot = Label(Voip_Frame_key_page, borderwidth=0, highlightthickness=0, image=logo_text).place(x=150, y=105)
    call = Label(Voip_Frame_key_page, text="Enter SecID", font='Helvetica 18 bold', foreground='gray',
                 background='white').place(x=190, y=200)
    ip = Entry(Voip_Frame_key_page, width=40, textvariable = dial)
    ip.place(x=145, y=230)

    Label(Voip_Frame_key_page, textvariable = status, font = 'Helvetica 12 bold').place(x = 200, y=270)

    # head = Label(Voip_Frame_key_page, text= "Attach key & click on textbox", font='Helvetica 18 bold', foreground= 'gray' , background = 'white').place(x=80, y= 230)

    # ip2= Entry(Voip_Frame_key_page,  width = 60)
    # ip2.place(x=60, y= 270)

    # keybutton=PhotoImage(file="key_button.gif")
    # a=Button(Voip_Frame_key_page,image=keybutton,bg='white')
    # a.place(x=210,y=320)

    # Voip_Frame_key_page['bg']='white'
    callbutton = PhotoImage(file="green_button.gif")
    b = Button(Voip_Frame_key_page, image=callbutton, bg='white', command = MakeCall)
    b.place(x=100, y=460)

    # Voip_Frame_key_page['bg']='white'
    endbutton = PhotoImage(file="red_button.gif")
    b = Button(Voip_Frame_key_page, image=endbutton, bg='white', command = CloseCall)
    b.place(x=300, y=460)
    
    
    

    Voip_Frame_key_page.mainloop()

    if(PT is not None):
       PT.CloseTerminal()

if __name__== '__main__':
     GUI()