# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 07:52:20 2019

@author: RayomandVatcha
"""
from __future__ import print_function, division, absolute_import, unicode_literals
#from Crypto.Cipher import AES
from SecuritySuite import AESCipher
import numpy

class PacketDetails:
    
    TotalSent = 0
    TotalRecieved = 0
    SendPacketSize = 0
    RecievePacketSize = 0
    @staticmethod
    def Details():
        print("Sent : Size = " + str(PacketDetails.SendPacketSize) + " Total = " + str(PacketDetails.TotalSent) +
        " Recieved : Size = " + str(PacketDetails.RecievePacketSize) + " Total = " + str(PacketDetails.TotalRecieved), end='\r')
        

class ProcessBytes:
    UserProfile = None

    def __init__(self):
        self.MaxOrderNumber = 16
        self.reInitialise()

    def reInitialise(self):
        self.OrderedBuffer = [None] * self.MaxOrderNumber
        self.lengthSeqNo = len(str(self.MaxOrderNumber))
        self.ctr = 0
        self.security_suite = None
        self.startPointer = -1
        self.rem = 0
        self.multiCastIncrementer = 0
        self.IsItP2P = True

    def enableKeyForGroupID(self, GroupID):
        if (ProcessBytes.UserProfile is None):
            key = "1234567890abcdef"
            print("[Alert :] Your call may not be secure as default key is being used. Please attach the physical key")
        else:
            key = ProcessBytes.UserProfile.getKey(GroupID)
        if(GroupID != "P2P"):
            self.IsItP2P = False
        else:
            self.IsItP2P = True
        self.security_suite = AESCipher(key)

    def NumberTheRawBytes(self, rawBytes):
        # print(len(rawBytes))
        self.ctr = (self.ctr + 1) % self.MaxOrderNumber
        dt = str(self.ctr).zfill(self.lengthSeqNo) + rawBytes
        # print(len(dt))
        # return dt
        #i = len(dt)
        #self.rem = min(16 - i % 16, i % 16)
        # print(self.rem)
        #for k in range(0, self.rem):
        #    dt = '0' + dt
        # print(len(dt))
        return dt

    def EncryptBytes(self, bytesData):
        if (self.security_suite is not None):
            dt = self.security_suite.encrypt(bytesData)
            return dt
        else:
            return bytesData

    def DecryptBytes(self, bytesData):
        return self.security_suite.decrypt(bytesData)

    def GetSeqNoData(self, bytesData):
        return bytesData[:self.lengthSeqNo + self.rem], bytesData[self.lengthSeqNo + self.rem:]

    def AddUnorderedBytes(self, packetData):
        # print(seqNo)

        if (packetData is None or len(packetData) == 0): return
        
        dataMultiple = []
        seqMultiple = []
        for bt in packetData:
            if (self.security_suite is not None):
                bytesData = self.DecryptBytes(bt)
            else:
                bytesData = bt
    
            seqNo, data = self.GetSeqNoData(bytesData)
            #print(seqNo)
            #print(len(data))
    
                # print(bytesData)
    
            er = seqNo.lstrip('0')
            if (len(er) == 0):
                seqNo = 0
            else:
                seqNo = int(er)
            # print(seqNo)
            dataMultiple.append(numpy.fromstring(data, dtype=numpy.uint8))
            seqMultiple.append(seqNo)

        if(self.IsItP2P):#len(dataMultiple) == 1):

            seqNo = seqMultiple[0]
            dataBlend = dataMultiple[0]
            self.OrderedBuffer[seqNo] = dataBlend.tostring()
            # print(self.OrderedBuffer)
            if (self.startPointer < 0 or self.startPointer >= self.MaxOrderNumber):
                self.startPointer = seqNo
        else:
            #print("**")
            ratio = 1.0 / len(dataMultiple)
            dataBlend = dataMultiple[0] #* ratio
            for dt in range(1, len(dataMultiple)):
                dataBlend = dataBlend + dataMultiple[dt] #* ratio
            #dataBlend = dataBlend.astype(numpy.uint8)

            #print(self.multiCastIncrementer)

            self.OrderedBuffer[self.multiCastIncrementer] = dataBlend.tostring()
            if (self.startPointer < 0 or self.startPointer >= self.MaxOrderNumber):
                self.startPointer = self.multiCastIncrementer
            self.multiCastIncrementer = self.multiCastIncrementer + 1
            if (self.multiCastIncrementer < 0 or self.multiCastIncrementer >= self.MaxOrderNumber):
                self.multiCastIncrementer = 0
            #self.startPointer = self.startPointer + 1
        
        return data

    def makeOrderedByte(self, rawData):
        bytesData = self.NumberTheRawBytes(rawData)
        bytesData = self.EncryptBytes(bytesData)
        #print(len(bytesData))
        return bytesData

    def getLatestOrderedByte(self):
        if (self.startPointer >= 0 and self.OrderedBuffer[self.startPointer] is not None):
            data = self.OrderedBuffer[self.startPointer]
            self.OrderedBuffer[self.startPointer] = None
            self.startPointer = self.startPointer + 1
            #print(self.startPointer)
            #print(self.OrderedBuffer)
            return data
        else:
            return None


if __name__ == "__main__":
    bytesData1 = 'A' * 10
    bytesData2 = 'B' * 10
    bytesData3 = 'C' * 10
    pr = ProcessBytes()
    pr.enableKeyForGroupID("P2P")
    b1 = pr.makeOrderedByte(bytesData1)
    print(b1)
    b2 = pr.makeOrderedByte(bytesData2)
    print(b2)
    b3 = pr.makeOrderedByte(bytesData3)
    print(b3)
    print("####################################")
    pr.AddUnorderedBytes(b2)
    pr.AddUnorderedBytes(b3)
    pr.AddUnorderedBytes(b1)
    while (True):
        tp = pr.getLatestOrderedByte()
        if (tp is not None):
            print(tp)
            print(pr.OrderedBuffer)



