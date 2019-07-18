# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:06:35 2019

@author: RayomandVatcha
"""

from TCPSender import MicUDPCommunicator
from TCPReciver import SpeakerUDPCommunicator
from CallersProfile import PersonProfile
from ProcessBytes import ProcessBytes, PacketDetails
from threading import Thread
from time import sleep
import usb.core
import usb.util
import math
try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

    
UsePhysicalKey = False
MultiCastGrp = '224.0.1.14'#'224.3.29.71'
MuliCastPortNo = 12346
PortNumber = 12345
isInterfaceAsKeyboard = False
network = b'eth0'
#network = b'wlan0'

     


class PhoneTerminal(Thread):

    def __init__(self, micDeviceID=-1, outDeviceID = -1):
        Thread.__init__(self)
        self.daemon = True 
        if(False):#make true to enable physical key
            ProcessBytes.UserProfile = PersonProfile(isInterfaceAsKeyboard)
            if(isInterfaceAsKeyboard):
                contents = input()
                ProcessBytes.UserProfile.AssignContents(contents)
        self.Talking = MicUDPCommunicator(micDeviceID=micDeviceID, network = network)
        self.Hearing = SpeakerUDPCommunicator(portNumber=PortNumber, network = network, SpeakerDeviceID = outDeviceID)
        self.ConnectionStatus = 'idle'
        self.Run = False
        self.CallersIP = None
        self.IP = self.Talking.IPAddress
        self.start()
        self.fnPrint = None
        
    def printC(self, message):
        if(self.fnPrint == None):
           print(message)
        else:
           self.fnPrint(message)
           print(message)
        
    def run(self):
        print("[Info :] Phone terminal service started")
        self.Run = True
        while(self.Run):
            try:
                sleep(1)
                if(self.ConnectionStatus == 'ConnectTo'):
                    self.printC("Hold on")
                    while (self.Hearing.ConnectionEstablished == False):
                            self.sine_tone(440, 0.2)
                            #print ".",
                            if(self.Run == False):
                              return
                            PacketDetails.Details()
                            if(self.ConnectionStatus=="Disconnect"):
                                break
                            if(self.IsPhysicalKeyConnected()==False):
                                     self.printC("[Alert :] Physical key not connected closing the call")
                                     self.ConnectionStatus = "Disconnect"
                                     break
                            sleep(1)
                    if (self.ConnectionStatus != "Disconnect"):
                        self.printC("The client " + str(self.Hearing.callerIP[0]) + " has just connected.. Please start talking")
                        self.Talking.clearBuffer()
                        self.ConnectionStatus = 'Talking'
                        self.WaitTillCallisDisconnected()
                    else:
                        self.printC("Idle. Make sure physical key is attached to the system")
                    self.Disconnect()
                    self.ConnectionStatus = 'idle'
                    
                    
                if (self.ConnectionStatus == 'idle'): 
                    self.CallersIP =  self.Hearing.callerIP
                    if(self.CallersIP is not None):
                         
                        print(self.Hearing.callerIP)
                        self.printC("Getting a call from " + str(self.Hearing.callerIP[0]))
                        self.ConnectionStatus = 'ringing'
                        while self.ConnectionStatus != 'pickup':                        
                             self.sine_tone(440, 0.1)
                             #print ".",
                             #i, o, e = select.select( [sys.stdin], [], [], 2)
                             #i = 1
                             #if (i):
                             #     
                             #     break
                             #     if (self.ConnectionStatus == "Disconnect"):
                             #         break
                             if (self.ConnectionStatus == "Disconnect"):
                                     break
                             if(self.Run == False):
                                return
                             if(self.IsPhysicalKeyConnected()==False):
                                     self.printC("[Alert :] Physical key not connected closing the call")
                                     self.ConnectionStatus = "Disconnect"
                                     break
                             PacketDetails.Details()
                             sleep(0.5)
                             #print("*")
                        self.printC( "You picked up phone..")
                        if (self.ConnectionStatus != "Disconnect"):
                               self.printC("The client " + str(self.Hearing.callerIP[0]) + " has just connected..")
                               self.Talking.ConnectTo(self.Hearing.callerIP[0], PortNumber)
                               self.Talking.clearBuffer()
                               self.ConnectionStatus = 'Talking'
                        else:
                            self.printC("Idle. Make sure physical key is attached to the system")
                        self.WaitTillCallisDisconnected()
                        self.Disconnect()
                        self.ConnectionStatus = 'idle'
                        self.CallersIP = None

                     
                 
                if(self.ConnectionStatus == 'Conference'):
                    self.printC("Hold on for participants to join")
                    while (self.Hearing.callerIP is None):
                        #print ".",
                        if(self.Run == False):
                              return
                        if (self.ConnectionStatus == "Disconnect"):
                            break
                        if(self.IsPhysicalKeyConnected()==False):
                                     self.printC("[Alert :] Physical key not connected closing the call")
                                     self.ConnectionStatus = "Disconnect"
                                     break
                        sleep(2)
                        PacketDetails.Details()
                    if (self.ConnectionStatus != "Disconnect"):
                        self.printC("The client " + str(self.Hearing.callerIP[0]) + " has just connected.. Please start talking")
                        self.ConnectionStatus = 'Talking'
                        self.WaitTillCallisDisconnected()
                    else:
                        self.printC("Idle")      
                    self.LeaveConference(MultiCastGrp, MuliCastPortNo)
                    self.ConnectionStatus = 'idle. Make sure physical key is attached to the system'
                    
                PacketDetails.Details()
        
            except KeyboardInterrupt:
               break
        
        
        
    def IsPhysicalKeyConnected(self):
        if(UsePhysicalKey ==False): return True

        self.device = usb.core.find(idVendor=0x16c0
                                    ,idProduct=0x27db)

        if self.device is not None:
                return True
        else:
                return False
    def ConnectTo(self, IPAddress):
        if(self.ConnectionStatus == 'idle' or self.ConnectionStatus == 'pickup'):
            self.Talking.ConnectTo(IPAddress, PortNumber)
            self.ConnectionStatus = 'ConnectTo'
            self.printC("Making connection...")
        else:
            self.printC("[Alert :] Please hang up current call")
            
    def WaitTillCallisDisconnected(self):
      while (True):
        try:
            sleep(1)
            if (self.Talking.ConnectionEstablished == False) :
                self.printC("[Info :] You have closed the connection")
                break
            if(self.Hearing.ConnectionEstablished == False):
                self.printC("[Info :] The reciver has disconnected")
                break
            if(self.Run == False):
                break
            if (self.ConnectionStatus == 'Disconnect'):
                   break
            if(self.IsPhysicalKeyConnected()==False):
                  self.printC("[Alert :] Physical key not connected closing the call")
                  break
            PacketDetails.Details()
        except KeyboardInterrupt:
            break

    def ConnectToConference(self, ConferenceIP, ConferencePortNo):
        if(self.ConnectionStatus == 'idle'):
            self.Talking.ConnectToMultiCastGroup(ConferenceIP, ConferencePortNo)
            self.Hearing.JointMulticastGroup(ConferenceIP, ConferencePortNo)
            self.ConnectionStatus = 'Conference'
        else:
            self.printC("[Alert :] Please hang up current call")
        
    def LeaveConference(self, ConferenceIP, ConferencePortNo):
        self.Hearing.LeaveMulticastGroup()
        self.Talking.LeaveMulticastGroup()

    def Disconnect(self):
        self.Talking.Disconnect()
        self.Hearing.Disconnect()

    def CloseTerminal(self):
        self.Run = False
        self.Disconnect()
        self.join()
        print("[Info :] Phone terminal is shutdown")
        self.Talking.ShutDownComplete()
        self.Hearing.ShutDownComplete()

    def sine_tone(self, frequency, duration, volume=1, sample_rate=48000):#22050):
        n_samples = int(sample_rate * duration)
        restframes = n_samples % sample_rate
    
        s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
        samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
        for buf in izip(*[samples]*sample_rate): # write several samples at a time
            self.Hearing.returnBytes(bytes(bytearray(buf)))
    
        # fill remainder of frameset with silence
        self.Hearing.returnBytes(b'\x80' * restframes)


def GroupCaller(DialTo, PortNo, micDeviceID=1):
    caller = PhoneTerminal(micDeviceID)
    if (True):
        # try:
        caller.ConnectToConference(DialTo, PortNo)
    

    caller.LeaveConference(DialTo, PortNo)



if __name__ == "__main__":

    MicUDPCommunicator.printListOfMicDevices()
    SpeakerUDPCommunicator.printListOfSpeakerDevices()
    micDeviceID = 0
    outDeviceID = 3
    areYouCaller = False
    isGroupCall = True
    
    caller = PhoneTerminal(micDeviceID, outDeviceID)
    sleep(2)

    if (isGroupCall):
        caller.ConnectToConference(MultiCastGrp, MuliCastPortNo)
    else:
        if (areYouCaller):
            caller.ConnectTo('10.8.0.6')

        else:
            print("Online")
            
    while (True):
        try:
            sleep(1)
            #print "*",
        except KeyboardInterrupt:
            print("Terminating")
            break
        
    #caller.Disconnect()
    caller.CloseTerminal()
    sleep(1)
   
