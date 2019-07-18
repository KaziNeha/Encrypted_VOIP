# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 09:53:03 2019

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

class TCPReciever(Thread):

    def __init__(self, network, portNumberToListen):
        Thread.__init__(self)
        self.daemon = True 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(0)
        self.sock.settimeout(2)

        self.Run = True;
        if ("Windows" not in platform.system()):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.IPAddress = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', network[:15])
            )[20:24])
        else:
            #hostname = socket.gethostname()  # socket.getfqdn()
            #self.IPAddress = socket.gethostbyname(hostname)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.IPAddress = s.getsockname()[0]
            s.close()
        self.name = "Recieve Thread @Your:IP:" + self.IPAddress
        self.sock.bind((self.IPAddress, portNumberToListen))
        self.ConnectionEstablished = False
        self.CHUNKSIZE = 4096*2 + 4
        # self.sock.settimeout(3)
        self.callerIP = None
        self.MulticastGrp = ""
        self.MulticastPortNo = 0
        self.portNumberToListen = portNumberToListen
        self.ByteProcessor = ProcessBytes()
        sleep(0.1)
        self.ConnectionEstablished = False

            

    def JointMulticastGroup(self, MulitcasteGrp, portNo):
        if(self.sock is not None):
           self.sock.close()
           
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.MulticastGrp = MulitcasteGrp
        self.MulticastPortNo = portNo

        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass

        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        print((self.MulticastGrp, self.MulticastPortNo))
        # self.sock.bind((self.MulticastGrp, self.MulticastPortNo))
        self.sock.bind(('0.0.0.0', self.MulticastPortNo))
        host = socket.gethostbyname(socket.gethostname())
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(self.MulticastGrp) + socket.inet_aton(host))
        self.ConnectionEstablished = True

    def LeaveMulticastGroup(self):
        host = socket.gethostbyname(socket.gethostname())
        self.sock.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                             socket.inet_aton(self.MulticastGrp) + socket.inet_aton(host))
        self.MulticastGrp = ""
        self.MulticastPortNo = 0
        self.sock.close()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(0)
        self.sock.settimeout(2)
        self.sock.bind((self.IPAddress, self.portNumberToListen))
        self.ConnectionEstablished = False
        self.callerIP = None

    def Disconnect(self):
        self.sock.close()
        self.ConnectionEstablished = False
        self.callerIP = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setblocking(0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.IPAddress, self.portNumberToListen))

        

    def receiveMessageFromTCP(self, conn):
        # print("*")
        # self.ConnectionEstablished = False
        data = conn.recv(4096)
        # data = conn.recv(1024)

        # datas = decryption_Suite.decrypt(data)
        return data

    def receiveMessageFromUDP(self):
        if (self.MulticastGrp == ""):
          while True:
            if(self.Run==False):
                        return None
            try:
                dg = self.sock.recvfrom(self.CHUNKSIZE )

                ds = dg[0]
                ipaddress = dg[1][0]
                self.callerIP = [str(ipaddress)]
                self.ConnectionEstablished = True
                #print(len(ds))
                return ds
            except socket.timeout:
                self.ConnectionEstablished = False
                continue                
            sleep(0.001)
        else:
         while True:
            if(self.Run==False):
                        return None
            try:
                dg, addr = self.sock.recvfrom(self.CHUNKSIZE)
                ds = dg[0]
                ipaddress = dg[1][0]
                if(self.callerIP is None):
                    self.callerIP= []
                    if(str(ipaddress) not in self.callerIP):
                        self.callerIP.append(str(ipaddress))
                if(self.callerIP[0] is not self.IPAddress):
                    break
            except socket.timeout:
                    self.ConnectionEstablished = False

         sleep(0.001)
         self.ConnectionEstablished = True
         return ds

    def RecieveMessage(self, BytesData):
        self.BufferMessg.append(BytesData)

    def returnBytes(self, bytesData):
        return 0

    def run(self):
        print("[Info :] Thread started for recieving streaming data..")
        ctr = 0
        while self.Run:
            #while self.ConnectionEstablished:
                try:
                    if(self.Run==False):
                        return
                    
                    # data = self.receiveMessageFromTCP(conn)
                    data = self.receiveMessageFromUDP()

                    if (data is None):
                        #self.ConnectionEstablished = False
                        ctr = ctr + 1
                        if(ctr > 100):
                            self.ConnectionEstablished = False
                        continue
                    else:
                        ctr = 0
                    self.ByteProcessor.AddUnorderedBytes(data)
                    rawSpeakerData = self.ByteProcessor.getLatestOrderedByte()
                    if(rawSpeakerData is not None):
                        self.returnBytes(rawSpeakerData)
                    else:
                        print "/",

                except socket.error as e:
                    print "[Error :] Recieveing packets. Closing current connection"
                    print(e)
                    self.ConnectionEstablished = False
                    break
                sleep(0.001)
        print("[Info :] Thread terminated for recieving streaming data..")

    def sendBytes(self, bytesData):
        self.sock.sendall(bytesData)

    def ShutDown(self):
        print("[Info :] Terminating UDPReceiver Thread")
        self.Run = False
        self.join()
        self.sock.close()
        print("[Info :] Terminated UDPReceiver Thread Successfully")


import pyaudio


class SpeakerTCPCommunicator(TCPReciever):

    def __init__(self, portNumber, network=b'wlan0'):
        TCPReciever.__init__(self, network=network, portNumberToListen=portNumber)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.speaker = self.p.open(format=self.FORMAT,
                                   channels=self.CHANNELS,
                                   rate=self.RATE,
                                   output=True,
                                   frames_per_buffer=4096)
        self.start()

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