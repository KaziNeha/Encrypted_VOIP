# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 09:53:03 2019

@author: RayomandVatcha
"""

import socket
from threading import Thread
from time import sleep
import platform
from ProcessBytes import ProcessBytes, PacketDetails


if ("Windows" not in platform.system()):
    import fcntl
import struct

class UDPReciever(Thread):
    
    def startListeningP2P(self):
            if(self.sock is not None):
                self.sock.close()
                self.sock = None
            print "Connecting",
            while self.RecievingON is not None:
                print ".",
                sleep(0.1)
            self.callerIP = None
            self.MulticastGrp = ""
            self.MulticastPortNo = 0
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setblocking(0)
            sock.settimeout(4)
            sock.bind((self.IPAddress, self.portNumberToListen))
            self.ConnectionEstablished = False
            self.ByteProcessor = ProcessBytes()
            self.ByteProcessor.enableKeyForGroupID("P2P")
            self.sock = sock
            

    def __init__(self, network, portNumberToListen):
        Thread.__init__(self)
        self.daemon = True
        self.sock = None
        self.Run = True;
        if True:
            #hostname = socket.gethostname()  # socket.getfqdn()
            #self.IPAddress = socket.gethostbyname(hostname)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.IPAddress = s.getsockname()[0]
            s.close()
        self.name = "Recieve Thread @Your:IP:" + self.IPAddress
        self.CHUNKSIZE = 64*1024 #4096*2 + 4
        self.portNumberToListen = portNumberToListen
        self.RecievingON = None
        
       
       

    def JointMulticastGroup(self, MulitcasteGrp, portNo):
        if (self.sock is not None):
            self.sock.close()
            #print(self.sock)
            self.sock = None
        self.ByteProcessor.reInitialise()
        self.ByteProcessor.enableKeyForGroupID(MulitcasteGrp)
        print "Joining",
        while self.RecievingON is not None:
            print ".",
            sleep(0.1)
        self.MulticastGrp = None
        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(0)
        sock.settimeout(0.02)
        self.MulticastPortNo = portNo
        multicast_group = (MulitcasteGrp, self.MulticastPortNo)
        server_address = ('', self.MulticastPortNo)
        # Bind to the server address
        sock.bind(server_address)
        self.MulticastGrp = MulitcasteGrp
        


        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(multicast_group[0])
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        print("[Info :] Added to the multicast group " + str(multicast_group[0]))
        self.sock = sock

        self.ConnectionEstablished = True


    def LeaveMulticastGroup(self):
        host = socket.gethostbyname(socket.gethostname())
        self.sock.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                             socket.inet_aton(self.MulticastGrp) + socket.inet_aton(host))
        self.MulticastGrp = ""
        self.MulticastPortNo = 0
        self.sock.close()
        self.sock = None
        
        self.startListeningP2P()

        

    def Disconnect(self):
        self.sock.close()
        self.sock = None
        self.startListeningP2P()

    def receiveMessageFromUDP(self):
        if(self.sock is None) : 
            sleep(0.1)
            return None
        
        if (self.MulticastGrp == ""):
          #print "wr"
          while True:
            if(self.Run==False):
                        return None
            self.RecievingON = "P2P"
            try:
                if(self.sock is None) :
                     self.RecievingON = None
                     return None
                dg = self.sock.recvfrom(self.CHUNKSIZE)

                
            except socket.timeout:
                self.ConnectionEstablished = False
                continue
                #return None            
            ds = dg[0]
            ipaddress = str(dg[1][0])
            #if (ipaddress == self.IPAddress):
            #        continue
            self.callerIP = [ipaddress]
            self.ConnectionEstablished = True
            #print(len(ds))
            self.RecievingON = None
            return [ds]
        else:
         self.RecievingON = "GROUP"
         recivedFromIP = []
         dataRecived = []
         while True:
                #print("rihht")
                while True:
                    if(self.Run==False):
                                return None
                    try:
                        if(self.sock is None) :
                             self.RecievingON = None
                             return None
                        dg = self.sock.recvfrom(self.CHUNKSIZE)
                        #print("rt")
                        break
                    except socket.timeout:
                            if(len(recivedFromIP) > 0):
                                return dataRecived

                            #self.ConnectionEstablished = False
                            continue
                ds = dg[0]
                #print(dg[1])
                ipaddress = str(dg[1][0])
                #print(ipaddress)
                if (ipaddress != self.IPAddress):
                    #print(self.IPAddress)
                    #print(ipaddress)
                    
                    if (self.callerIP is None):
                        self.callerIP = []
                    if (ipaddress not in self.callerIP):
                            self.callerIP.append(ipaddress)
                            print(ipaddress+ ":" + str(dg[1][1])  + " has joined")
                    if(ipaddress in recivedFromIP):
                        break
                    else:
                        dataRecived.append(ds)
                        recivedFromIP.append(ipaddress)
                        
                    
         self.ConnectionEstablished = True
         self.RecievingON = None
         return dataRecived

    def RecieveMessage(self, BytesData):
        self.BufferMessg.append(BytesData)

    def returnBytes(self, bytesData):
        return 0

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

    def sendBytes(self, bytesData):
        self.sock.sendall(bytesData)

    def ShutDown(self):
        print("[Info :] Terminating UDPReceiver Thread")
        self.Run = False
        self.join()
        if (self.sock is not None):
            self.sock.close()        
        print("[Info :] Terminated UDPReceiver Thread Successfully")


import pyaudio


class SpeakerUDPCommunicator(UDPReciever):
    
    @staticmethod
    def printListOfSpeakerDevices():
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                print "Output Device id ",p.get_device_info_by_host_api_device_index(0, i).get('index') , " - ", p.get_device_info_by_host_api_device_index(0, i).get('name') , " # Channels =" , p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')


    def __init__(self, portNumber, network=b'wlan0', SpeakerDeviceID = -1):
        UDPReciever.__init__(self, network=network, portNumberToListen=portNumber)
        self.FORMAT = pyaudio.paInt16
        #self.CHANNELS = 1
        self.RATE = 48000#44100
        self.p = pyaudio.PyAudio()
        if(SpeakerDeviceID < 0):
            SpeakerDeviceID = self.p.get_default_output_device_info().get('index')
        print("[Info :] Output Device selected : " + str(self.p.get_device_info_by_host_api_device_index(0, SpeakerDeviceID).get('name'))) 
        self.CHANNELS = min(2, self.p.get_device_info_by_host_api_device_index(0, SpeakerDeviceID).get('maxOutputChannels'))
        self.speaker = self.p.open(format=self.FORMAT,
                                   channels=self.CHANNELS,
                                   rate=self.RATE,
                                   output=True,
                                   output_device_index = SpeakerDeviceID,
                                   frames_per_buffer=2048)
        self.start()
        self.startListeningP2P()
        

    def returnBytes(self, bytesData):
       # print(bytesData)
        self.speaker.write(bytesData)

    def CloseMic(self):
        self.speaker.stop_stream()
        self.speaker.close()
        # self.p.terminate()

    def ShutDownComplete(self):
        self.CloseMic()
        self.p.terminate()
        #self.Disconnect()
        self.ShutDown()
