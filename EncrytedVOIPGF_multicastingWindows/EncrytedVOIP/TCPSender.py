# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 09:12:27 2019

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


class UDPSender(Thread):

    def __init__(self, network):
        Thread.__init__(self)
        self.sock = None
        self.BufferMessg = []
        self.Run = True;
        self.daemon = True 
        print(platform.system())
        if True:
            #hostname = socket.gethostname()  # socket.getfqdn()
            #self.IPAddress = socket.gethostbyname(hostname)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.IPAddress = s.getsockname()[0]
            s.close()
        self.name = "Send Thread @Your:IP:" + self.IPAddress
        print("[Running :] " + self.name)
        self.ConnectionEstablished = False
        self.MulticastAddress = ""
        self.rawByteProcessor = ProcessBytes()
        self.ConnectToIPAddress = ""
        self.ConnectToPortNo = 0

    def ConnectTo(self, IPAddress, PortNumber):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.rawByteProcessor.reInitialise()
        self.rawByteProcessor.enableKeyForGroupID("P2P") 
        #self.sock.connect((IPAddress, PortNumber))
        print("Connecting + " + IPAddress + "...")
        self.ConnectToIPAddress = IPAddress
        self.ConnectToPortNo = PortNumber
        self.ConnectionEstablished = True

    def ConnectToMultiCastGroup(self, GrpAddress, PortNumber):
        self.MulticastAddress = GrpAddress
        self.PortNo = PortNumber
        self.rawByteProcessor.reInitialise()
        self.rawByteProcessor.enableKeyForGroupID(GrpAddress)
        multicast_group = (self.MulticastAddress,  self.PortNo)

        # Create the datagram socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        self.sock.settimeout(0.2)

        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        print("Connection established...")
        self.ConnectionEstablished = True

    def ConnectToMultiCastGroup1(self, GrpAddress, PortNumber):
        self.rawByteProcessor.reInitialise()
        self.rawByteProcessor.enableKeyForGroupID(GrpAddress)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.IPAddress))
        self.MulticastAddress = GrpAddress
        self.PortNo = PortNumber
        # self.sock.connect((IPAddress, PortNumber))
        print("Connection established...")
        self.ConnectionEstablished = True
        

    def LeaveMulticastGroup(self):
        self.MulticastAddress = ""
        self.PortNo = 0
        self.ConnectionEstablished = False

    def clearBuffer(self):
        self.BufferMessg = []
        
    def Disconnect(self):
        if (self.sock is not None):
            self.sock.close()
            self.BufferMessg = []
            self.ConnectionEstablished = False
            self.sock = None

    def SendMessage(self, BytesData):
        self.BufferMessg.append(BytesData)

    def getBytes(self):
        return 0

    def run(self):
        print("[Info :] Thread started for sending streaming data..")
        while self.Run:
            rawMicData = self.getBytes()            
            #if (self.ConnectionEstablished):
            if (rawMicData is not None ):
              try:
                    #dataToSend = rawMicData
                    dataToSend = self.rawByteProcessor.makeOrderedByte(rawMicData)
                    #print (len(dataToSend))
                    self.sendBytes(dataToSend)
                    #print(len(self.BufferMessg))
              except Exception as e:
                    print("[Warning :] Sender Thread --> " + str(e))
                    #x=0
            else:
                  print "?",
        print("[Info :] Thread terminated for sending streaming data..")

    def sendBytes(self, bytesData):
        if(self.sock is None): 
            sleep(0.1)
            return
        try:

            PacketDetails.SendPacketSize = len(bytesData)
            PacketDetails.TotalSent = PacketDetails.TotalSent + 1
            if (self.MulticastAddress == ""):
                #print(len(bytesData))
                st = self.sock.sendto(bytesData, (self.ConnectToIPAddress, self.ConnectToPortNo))
            else:
                st = self.sock.sendto(bytesData, (self.MulticastAddress, self.PortNo))
            # print( str(st) + " bytes sent\r")
        except socket.timeout:
            self.ConnectionEstablished = False

    def ShutDown(self):
        print("[Info :] Terminating UDPSender Thread")
        self.Run = False
        self.join()
        if (self.sock is not None):
            self.sock.close()
        print("[Info :] UDP Sender Thread Successfully closed ")


import pyaudio


class MicUDPCommunicator(UDPSender):

    @staticmethod
    def printListOfMicDevices():
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print "Input Device id ", p.get_device_info_by_host_api_device_index(0, i).get('index') , " - ", p.get_device_info_by_host_api_device_index(0, i).get('name') , " # Channels =" , p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')
                #print(p.get_device_info_by_host_api_device_index(0, i))

    def __init__(self, micDeviceID=-1, network=b'wlan0'):
        UDPSender.__init__(self,network=network)
        self.CHUNK =  2048
        self.FORMAT = pyaudio.paInt16
        #self.CHANNELS = 1
        self.RATE = 48000#44100
        self.p = pyaudio.PyAudio()
        if(micDeviceID < 0):
            micDeviceID = self.p.get_default_input_device_info().get('index')
        print("[Info :] Input Device selected : " + str(self.p.get_device_info_by_host_api_device_index(0, micDeviceID).get('name')))
        self.CHANNELS = min (2, self.p.get_device_info_by_host_api_device_index(0, micDeviceID).get('maxInputChannels'))
        self.mic = self.p.open(format=self.FORMAT,
                               channels=self.CHANNELS,
                               rate=self.RATE,
                               input=True,
                               input_device_index=micDeviceID,
                               frames_per_buffer=self.CHUNK)
        #self.mic.neverDropInput = False
        self.start()

    def getBytes(self):
        #try:
        data = self.mic.read(self.CHUNK, exception_on_overflow = False)
        #except Exception as ex:
        #    return None
        #print len(data),
        return data
        #print(len(self.BufferMessg))
        #print(len(data))

    def CloseMic(self):
        self.mic.stop_stream()
        self.mic.close()
        # self.p.terminate()

    def ShutDownComplete(self):
        self.CloseMic()
        self.ShutDown()
        #self.Disconnect()

if __name__== '__main__':
    m= MicTCPCommunicator(2)
    
