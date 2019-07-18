# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 07:52:20 2019

@author: RayomandVatcha
"""
from Crypto.Cipher import AES


class ProcessBytes:
    UserProfile = None

    def __init__(self):
        self.MaxOrderNumber = 16
        self.lengthSeqNo = len(str(self.MaxOrderNumber))
        self.OrderedBuffer = [None] * self.MaxOrderNumber
        self.ctr = 0
        self.security_suite = None
        self.startPointer = -1
        self.rem = 2

    def reInitialise(self):
        self.OrderedBuffer = [None] * self.MaxOrderNumber
        self.lengthSeqNo = len(str(self.MaxOrderNumber))
        self.ctr = 0
        self.security_suite = None
        self.startPointer = -1
        self.rem = 2

    def enableKeyForGroupID(self, GroupID):
        return
        if (ProcessBytes.UserProfile is None):
            key = "1234567890abcdef"
            print("[Alert :] Your call may not be secure as default key is being used. Please attach the physical key")
        else:
            key = ProcessBytes.UserProfile.getKey(GroupID)
        self.security_suite = AES.new(key, AES.MODE_CBC, 'This is an IV456')

    def NumberTheRawBytes(self, rawBytes):
        # print(len(rawBytes))
        self.ctr = (self.ctr + 1) % self.MaxOrderNumber
        dt = str(self.ctr).zfill(self.lengthSeqNo) + rawBytes
        # print(len(dt))
        # return dt
        i = len(dt)
        self.rem = min(16 - i % 16, i % 16)
        # print(self.rem)
        for k in range(0, self.rem):
            dt = '0' + dt
        # print(len(dt))
        return dt

    def EncryptBytes(self, bytesData):

        # print(len(bytesData))
        if (self.security_suite is not None):
            dt = self.security_suite.encrypt(bytesData)
            # print(len(dt))
            return dt
        else:
            return bytesData

    def DecryptBytes(self, bytesData):
        return self.security_suite.decrypt(bytesData)

    def GetSeqNoData(self, bytesData):
        return bytesData[:self.lengthSeqNo + self.rem], bytesData[self.lengthSeqNo + self.rem:]

    def AddUnorderedBytes(self, bytesData):
        # print(seqNo)
        if (bytesData is None or len(bytesData) == 0): return

        seqNo, data = self.GetSeqNoData(bytesData)
        #print(seqNo)
        #print(len(data))
        if (self.security_suite is not None):
            data = self.DecryptBytes(data)
            # print(bytesData)

        er = seqNo.lstrip('0')
        if (len(er) == 0):
            seqNo = 0
        else:
            seqNo = int(er)
        # print(seqNo)
        self.OrderedBuffer[seqNo] = data
        # print(self.OrderedBuffer)
        if (self.startPointer < 0 or self.startPointer >= self.MaxOrderNumber):
            self.startPointer = seqNo
        return data

    def makeOrderedByte(self, rawData):
        bytesData = self.EncryptBytes(rawData)
        bytesData = self.NumberTheRawBytes(bytesData)
        # print(len(bytesData))
        return bytesData

    def getLatestOrderedByte(self):
        if (self.startPointer >= 0 and self.OrderedBuffer[self.startPointer] is not None):
            data = self.OrderedBuffer[self.startPointer]
            self.OrderedBuffer[self.startPointer] = None
            self.startPointer = self.startPointer + 1
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



