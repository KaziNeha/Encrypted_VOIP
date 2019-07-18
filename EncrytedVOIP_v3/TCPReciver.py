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

    def __init__(self, network=b'wlan0', portNumberToListen=1234):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.bind(("0.0.0.0",portNumberToListen))
        self.Run = True;
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
        print("[Running :] " + self.name)
        self.ConnectionEstablished = False
        self.CHUNKSIZE = 1024
        # self.sock.settimeout(3)
        self.callerIP = ""
        self.MulticastGrp = ""
        self.MulticastPortNo = 0
        self.portNumberToListen = portNumberToListen
        self.ByteProcessor = ProcessBytes()
        sleep(0.1)
            

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
        self.sock.bind(("0.0.0.0", self.portNumberToListen))
        self.ConnectionEstablished = False

    def Disconnect(self):
        self.sock.close()
        self.ConnectionEstablished = False

    def receiveMessageFromTCP(self, conn):
        # print("*")
        # self.ConnectionEstablished = False
        data = conn.recv(4096)
        # data = conn.recv(1024)

        # datas = decryption_Suite.decrypt(data)
        return data

    def receiveMessageFromUDP(self):
        if (self.MulticastGrp == ""):

            dg = self.sock.recvfrom(4096)
            ds = dg[0]
            ipaddress = dg[1][0]
            self.callerIP = [str(ipaddress)]
            self.ConnectionEstablished = True
            return ds
        else:
            ds, addr = self.sock.recvfrom(4096)
            self.ConnectionEstablished = True
            return ds

    def RecieveMessage(self, BytesData):
        self.BufferMessg.append(BytesData)

    def returnBytes(self, bytesData):
        return 0

    def run(self):
        print("[Info :] Thread started for recieving streaming data..")
        while self.Run:
            # try:
            # self.sock.listen(1)
            # conn, addr = self.sock.accept()
            # except socket.timeout:
            #   self.ConnectionEstablished = False
            #   continue

            # if(addr != self.callerIP ):
            # self.callerIP = addr
            # self.ConnectionEstablished= True
            while self.ConnectionEstablished:
                try:
                    # data = self.receiveMessageFromTCP(conn)
                    data = self.receiveMessageFromUDP()
                    self.ByteProcessor.AddUnorderedBytes(data)
                    if (data is None):
                        self.ConnectionEstablished = False
                        break
                    rawSpeakerData = self.ByteProcessor.getLatestOrderedByte()
                    if(rawSpeakerData is not None):
                        self.returnBytes(rawSpeakerData)

                except socket.error as e:
                    print "[Error :] Recieveing packets. Closing current connection"
                    print(e)
                    self.ConnectionEstablished = False
                    break
            sleep(0.001)
        print("[Info :] Thread terminated for recieving streaming data..")

    def sendBytes(self, bytesData):
        self.sock.sendall(bytesData)

    def __del__(self):
        print("[Info :] Terminating TCPReceiver Thread")
        self.Run = False
        self.join()
        self.sock.close()


import pyaudio


class SpeakerTCPCommunicator(TCPReciever):

    def __init__(self, portNumber):
        TCPReciever.__init__(self, portNumberToListen=portNumber)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.speaker = self.p.open(format=self.FORMAT,
                                   channels=self.CHANNELS,
                                   rate=self.RATE,
                                   output=True,
                                   frames_per_buffer=self.CHUNKSIZE)
        self.start()

    def returnBytes(self, bytesData):
        self.speaker.write(bytesData)

    def CloseMic(self):
        self.speaker.stop_stream()
        self.speaker.close()
        # self.p.terminate()

    def __del__(self):
        self.CloseMic()
        self.p.terminate()
        self.Disconnect()