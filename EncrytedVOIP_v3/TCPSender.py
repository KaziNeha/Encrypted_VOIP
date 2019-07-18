# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 09:12:27 2019

@author: RayomandVatcha
"""
import socket
from threading import Thread
from time import sleep
import platform
from ProcessBytes import ProcessBytes


if ("Windows" not in platform.system()):
    import fcntl
import struct


class TCPSender(Thread):

    def __init__(self, network=b'wlan0'):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.BufferMessg = []
        self.Run = True;
        print(platform.system())
        if ("Windows" not in platform.system()):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.IPAddress = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', network[:15])
            )[20:24])
        else:
            hostname = socket.gethostname()  # socket.getfqdn()
            self.IPAddress = socket.gethostbyname(hostname)
        self.name = "TCPSender:IP:" + self.IPAddress
        print("[Running :] " + self.name)
        self.ConnectionEstablished = False
        self.MulticastAddress = ""
        self.rawByteProcessor = ProcessBytes()

    def ConnectTo(self, IPAddress, PortNumber):
        self.rawByteProcessor.reInitialise()
        self.rawByteProcessor.enableKeyForGroupID("P2P") 
        self.sock.connect((IPAddress, PortNumber))
        print("Connection established...")
        self.ConnectionEstablished = True
        

    def ConnectToMultiCastGroup(self, GrpAddress, PortNumber):
        self.rawByteProcessor.reInitialise()
        self.rawByteProcessor.enableKeyForGroupID(GrpAddress)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
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
        if (self.ConnectionEstablished):
            self.sock.close()
            self.BufferMessg = []
            self.ConnectionEstablished = False

    def SendMessage(self, BytesData):
        self.BufferMessg.append(BytesData)

    def getBytes(self):
        return 0

    def run(self):
        print("[Info :] Thread started for sending streaming data..")
        while self.Run:
            self.getBytes()            
            if (self.ConnectionEstablished):
                if (len(self.BufferMessg) > 0):
                    rawMicData = self.BufferMessg[0]
                    dataToSend = self.rawByteProcessor.makeOrderedByte(rawMicData)
                    self.sendBytes(dataToSend)
                    del self.BufferMessg[0]
            sleep(0.001)
        print("[Info :] Thread terminated for sending streaming data..")

    def sendBytes(self, bytesData):
        try:

            
            if (self.MulticastAddress == ""):
                st = self.sock.send(bytesData)
            else:
                st = self.sock.sendto(bytesData, (self.MulticastAddress, self.PortNo))
            # print( str(st) + " bytes sent\r")
        except socket.timeout:
            self.ConnectionEstablished = False

    def __del__(self):
        print("[Info :] Terminating TCPSender Thread")
        self.Run = False
        self.join()
        if (self.ConnectionEstablished):
            self.sock.close()


import pyaudio


class MicTCPCommunicator(TCPSender):

    @staticmethod
    def printListOfMicDevices():
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name')

    def __init__(self, micDeviceID=1):
        TCPSender.__init__(self)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.mic = self.p.open(format=self.FORMAT,
                               channels=self.CHANNELS,
                               rate=self.RATE,
                               input=True,
                               input_device_index=micDeviceID,
                               frames_per_buffer=self.CHUNK)
        self.start()

    def getBytes(self):
        data = self.mic.read(self.CHUNK)
        self.SendMessage(data)
        #print(data)

    def CloseMic(self):
        self.mic.stop_stream()
        self.mic.close()
        # self.p.terminate()

    def __del_(self):
        self.CloseMic()
        self.Disconnect()

