# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 07:52:20 2019

@author: RayomandVatcha
"""
from Crypto.Cipher import AES
from threading import Thread
import base64

class ProcessBytes:
    
    def __init__(self):
        self.MaxOrderNumber = 16
        self.lengthSeqNo = len(str(self.MaxOrderNumber))
        self.OrderedBuffer = [] * self.MaxOrderNumber
        self.ctr = 0
        self.security_suite = None
        self.startPointer = -1
    
    def reInitialise(self):
        self.OrderedBuffer = [] * self.MaxOrderNumber
        self.ctr = 0
        self.security_suite = None
        self.startPointer = -1
        
    def enableKeyForGroupID(self, GroupID):
        key = "123456"
        self.security_suite = AES.new(key, AES.MODE_OFB, 'This is an IV456')
        
        
    def NumberTheRawBytes(self, rawBytes):
        self.ctr = (self.ctrl + 1) % self.MaxOrderNumber
        return str(self.ctr).zfill(self.lengthSeqNo) + rawBytes
        
    def EncryptBytes(self, bytesData):
        if(self.security_suite is not None):
           return self.security_suite.encrypt(bytesData)
        else:
            return bytesData
    
    def DecryptBytes(self, bytesData):
        return self.security_suite.decrypt(bytesData)
    
    def GetSeqNoData(self, bytesData):
        return bytesData[:self.lengthSeqNo], bytesData[self.lengthSeqNo:]
    
    def AddUnorderedBytes(self, bytesData):
        if(self.security_suite is not None):
            bytesData = self.DecryptBytes(bytesData)
        seqNo, data = self.GetSeqNoData(bytesData)
        self.OrderedBuffer[int(seqNo)] = data
        if(self.startPointer < 0 or self.startPointer >= self.MaxOrderNumber):
           self.startPointer = seqNo
        return data
    
    def makeOrderedByte(self, rawData):
        bytesData = self.NumberTheRawBytes(rawData)
        bytesData = self.EncryptBytes(bytesData)
        return bytesData
            
    
    def getLatestOrderedByte(self):
        if(self.OrderedBuffer[self.startPointer] is not None):
            data = self.OrderedBuffer[self.startPointer]
            self.OrderedBuffer[self.startPointer] = None
            self.startPointer = self.startPointer + 1
            return data
        else:
            return None
            