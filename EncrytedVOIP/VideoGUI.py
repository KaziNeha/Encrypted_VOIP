# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:01:32 2019

@author: RayomandVatcha
"""
import tkinter as tk
from tkinter import *
import numpy
import cv2
from time import sleep
from TCPReciver import UDPReciever
from TCPSender import UDPSender
import array
from math import ceil
import socket
from ProcessBytes import  PacketDetails
from time import clock

class WebcamSender(UDPSender):
    
    def __init__(self, Width = 640, Height= 480, cameraIndex = 0):
        UDPSender.__init__(self, "eth0")
        self.CHUNKSIZE = 16*1024 - 2
        self.camera = cv2.VideoCapture(cameraIndex)
        self.Width = Width
        self.Height = Height
        self.start()
        
    def getBytes(self):
        rawFrame = self.camera.read()[1]
        rawFrame =  cv2.resize(rawFrame, (self.Width, self.Height))
        rawFrame = cv2.cvtColor(rawFrame, cv2.COLOR_BGR2RGB)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, rawFrame = cv2.imencode('.jpg', rawFrame, encode_param)
        BytesData = rawFrame.flatten()
        if(BytesData.size > self.CHUNKSIZE):
           BytesData = numpy.array_split(BytesData,int(ceil( BytesData.size/ self.CHUNKSIZE)))
        else:
            BytesData = [BytesData]
        #print BytesData
        #sleep(10)
        return BytesData
    
    def run(self):
        print("[Info :] Thread started for sending streaming data..")
        while self.Run:
            rawImageDataList = self.getBytes()            
            #if (self.ConnectionEstablished):
            for rawData in rawImageDataList:
                rawData = rawData.tostring()
                if (rawData is not None ):
                  try:
                        #dataToSend = rawData
                        dataToSend = self.rawByteProcessor.makeOrderedByte(rawData)
                        #print (len(dataToSend))
                        self.sendBytes(dataToSend)
                        PacketDetails.Details()
                        #print(len(self.BufferMessg))
                  except Exception as e:
                        print("[Warning :] Sender Thread --> " + str(e))
                        #x=0
                else:
                      print "?",
            rawData = "EndImageEndImageEndImageEndImageEndImageEndImage"
            dataToSend = self.rawByteProcessor.makeOrderedByte(rawData)
            self.sendBytes(dataToSend)
            sleep(0.1)
           
        print("[Info :] Thread terminated for sending streaming data..")
        
    
    def __del__(self):
         self.camera.release()
         del self.camera
        

class WebcamRemoteReciever(UDPReciever):
    
    def __init__(self, portNumberToListen, Width = 640, Height= 480):
        UDPReciever.__init__(self, "eth0", portNumberToListen)
        self.NoChunks1Image = int(ceil(Width*Height*3.0 / (16*1024-2)))
        self.ctr = 0
        self.Image= None
        self.ImageReady = [0] * (Width*Height*3)
        self.start()
        self.startListeningP2P()
        self.prevT = clock()
        
    def returnBytes(self, bytesData):
        if(bytesData == "EndImageEndImageEndImageEndImageEndImageEndImage"):
            self.ctr = self.NoChunks1Image
        
        bytesData = array.array('B', bytesData)
        if(self.ctr == self.NoChunks1Image):
            dc = cv2.imdecode(numpy.array(self.Image), 1)
            self.ImageReady = dc.flatten()# self.Image
            self.ctr = 0
            #print("FPS = " + str(1.0/(clock()-self.prevT)))
            self.prevT =clock()
            return
            
        if(self.ctr == 0):
           self.Image = bytearray()
           self.Image.extend(bytesData)
        else:
            self.Image.extend(bytesData)
        
        #print(self.ctr)
        self.ctr = self.ctr + 1
        
    def read(self):
        #sleep(0.1)
        return True, self.ImageReady
    
    def run(self):
        print("[Info :] Thread started for recieving streaming data..")
        ctr = 0
        while self.Run:
                try:
                    data = self.receiveMessageFromUDP()
                    

                    if (data is None):
                        ctr = ctr + 1
                        if(ctr > 1000):
                            self.ConnectionEstablished = False
                        continue
                    else:
                        ctr = 0
                    
                    PacketDetails.RecievePacketSize = len(data[0])
                    PacketDetails.TotalRecieved =PacketDetails.TotalRecieved + 1 
                    
                    #if(PacketDetails.RecievePacketSize[0] > 0 and PacketDetails.RecievePacketSize[0] != PacketDetails.SendPacketSize):
                        #print("[Warning :] Recieved packet of incorrect size")
                    #    continue
                    
                    #rawSpeakerData = numpy.fromstring(data[0], dtype=numpy.uint8).tolist()
                    self.ByteProcessor.AddUnorderedBytes(data)
                    rawSpeakerData = self.ByteProcessor.getLatestOrderedByte()
                    if(rawSpeakerData is not None):
                        self.returnBytes(rawSpeakerData)
                    else:
                        #print "/",
                        x=0

                except socket.error as e:
                    print "[Error :] Recieveing packets"
                    print(e)
                    self.ConnectionEstablished = False
                    break
                
        print("[Info :] Thread terminated for recieving streaming data..")



class ImageDisplayCanvas(Label):

    #data = numpy.array(numpy.random.random((480, 640))*900,dtype=numpy.uint16)

    def __init__(self, Width, Height, parent):
        Label.__init__(self, parent, width=Width, height = Height)
        self.root = parent
        self.width =  Width #self.winfo_width()
        self.height = Height #self.winfo_height();
        self.grid(row=0, column=0)
        self.initialise()
        self.pack()
        mystring = 'P6 ' + str(self.width) + ' ' + str(self.height) +' 255 '
        self.header =  bytearray()
        self.header.extend(mystring)#.decode('ascii')
        self.ctr= 0
       

    def initialise(self):
        self.photo = tk.PhotoImage(master = self, width=self.width, height=self.height, format='PPM')#, data = b'P6 640 480 255 ' + self.data.tobytes())
        #self.imid = self.create_image(0,0,image=self.photo, anchor=tk.NW)
        
    def Update(self, byteData):
        #global data
        bytesData = bytearray()
        bytesData.extend(self.header)
        bytesData.extend(byteData)
        del self.photo
        sleep(0.15)
        self.photo = tk.PhotoImage(master = self, width=self.width, height=self.height, format='PPM', data= bytesData )#.tobytes())
        #self.itemconfig(self.imid,  image = self.photo)
        self.configure(image = self.photo)
        
        #if True:
        #    self.itemconfig(self.imid, image = self.photo)
        #else:
        #self.delete(self.imid)
        #self.imid = self.create_image(0,0,image=self.photo,anchor=tk.NW)




class VideoGUI(Frame):

    def __init__(self,  Width, Height, imageWidth, imageHeight, master = None, cnf = {}, **kw):
        Frame.__init__(self, master, width=Width, height=Height)
        self.root = master
        self.width = Width
        self.height = Height
        self.ImgWidth = imageWidth
        self.ImgHeight = imageHeight
        self.initialise()


    def initialise(self):
        
        self.byteRGB24Data = 0
        self.imageRender = ImageDisplayCanvas(parent = self, Width = self.ImgWidth, Height = self.ImgHeight)
        self.pack()

    def startCamera(self, cam):
        self.cam = cam
        #self.output = picamera.array.PiRGBArray(self.cam)
        #self.cam.start()
    def Loop(self):
        if(self.cam):
            self.image = self.cam.read()[1]
            self.image = numpy.array(self.image)
            self.byteRGB24Data = self.image.flatten() # [0 for i in range(self.ImgWidth*self.ImgHeight*3)]
            del self.image
            ##c = 0
            #for i in range(0,self.ImgHeight):
             #   for j in range(0, self.ImgWidth):
              #      for k in range(0, 3):
               #         self.byteRGB24Data[c]= self.image[i][j][k]
                #        c += 1
            self.imageRender.Update(self.byteRGB24Data.tobytes())
            if(self.cam):
                self.update()
                self.root.update()
                self.root.after(0,self.Loop)
                

    #def on_closing(self):
    #    self.cam.release()
    #    self.deletecommand(cam)
        
    def __del__(self):
        self.cam.release()        
        #if(self.cam):
         #   self.cam.release()

if __name__=='__main__':
    
    VideoPortNo = 12348
    camera = WebcamRemoteReciever(VideoPortNo)
    sleep(1) 
    sender =  WebcamSender()
    
    sender.ConnectTo('192.168.1.101', VideoPortNo)
    sleep(1)
    root = tk.Tk()
    frame = VideoGUI(master = root, Width = 640, Height = 480, imageWidth = 640, imageHeight=480)
    frame.startCamera(camera)
    frame.pack()
    root.after(0,frame.Loop)
    root.mainloop()
    sleep(1)
    camera.ShutDown()
    sender.ShutDown()
   
    


if __name__=='__main1__':
    

    
    camera  = cv2.VideoCapture(0)
    root = tk.Tk()
    frame = VideoGUI(master = root, Width = 640, Height = 480, imageWidth = 640, imageHeight=480)
    frame.startCamera(camera)
    frame.pack()
    root.after(0,frame.Loop)
    root.mainloop()
    sleep(1)
    camera.release()