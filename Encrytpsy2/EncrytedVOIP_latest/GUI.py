from Tkinter import *
import Tkinter
from PIL import Image, ImageTk
import os
import threading

from TCPSender import MicUDPCommunicator
from TCPReciver import SpeakerUDPCommunicator
from CallersProfile import PersonProfile
from ProcessBytes import ProcessBytes, PacketDetails, PersonProfile
from threading import Thread
from time import sleep
import math
from CallerMain import PhoneTerminal

def GUI():

    Voip_Frame = Tk()
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
        sleep(2)

    def MakeCall():
        global PT
        if(PT.ConnectionStatus != 'ringing'):
           PT.ConnectTo(dial.get())
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

    
    Voip_Frame.title("GoSecure")
    Voip_Frame.geometry('900x500')
    Voip_Frame.configure(background = 'gray15')
    head = Label(Voip_Frame, text= "Make Encrypted Calls!", font='Helvetica 18 bold', foreground= 'white' , background = 'gray15').place(x=300, y= 10)
    logo=ImageTk.PhotoImage(Image.open("wall.JPG"))
    logoLbl = Label(Voip_Frame, borderwidth= 0, highlightthickness = 0, image=logo).place(x=320, y=65)
    call = Label(Voip_Frame, text= "Enter goSecure id to make a call", font='Helvetica 15', foreground= 'white' , background = 'gray15').place(x=260, y= 260)
    
    
    ip= Entry(Voip_Frame,  width = 60, textvariable = dial)
    ip.place(x=250, y= 320)

    acpt = Button(Voip_Frame, width = 4, height = 1, text = "Key", font = 'bold', command = EnterPhysicalKeyDetails)
    acpt.config(background = 'gray')
    acpt.place(x = 650, y= 315)

    call = Button(Voip_Frame, width = 10, text = "Call", font = 'bold', command =MakeCall )
    call.config(background = 'green')
    call.place(x=270 , y = 380)
    stop = Button(Voip_Frame, width = 10, text = "Stop", font = 'bold', command = CloseCall)
    stop.config(background = 'red')
    stop.place(x=450 , y = 380)
    
    call = Label(Voip_Frame, textvariable= status, font='Helvetica 8', foreground= 'white' , background = 'gray15').place(x=320, y= 440)



    #lb = Listbox(Voip_Frame, height = 31, width = 30)
    #lb.config(background = 'white', font = 'Helveltica 15 bold')
    #lb.place(x = 716, y= 0)
    #lb.insert(1,"Your groups")
    #lb.insert(2, "")
    #lb.insert(2,"Group 1")
    #lb.insert(3, "Group 2")

    Voip_Frame.mainloop()
    if(PT is not None):
       PT.CloseTerminal()

if __name__== '__main__':
     GUI()
