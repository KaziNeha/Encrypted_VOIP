# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:06:35 2019

@author: RayomandVatcha
"""

from TCPSender import MicTCPCommunicator
from TCPReciver import SpeakerTCPCommunicator
from time import sleep

MultiCastGrp = '224.1.1.1'
MuliCastPortNo = 12346
PortNumber = 12345


class PhoneTerminal:

    def __init__(self, micDeviceID=0):
        self.Talking = MicTCPCommunicator(micDeviceID=micDeviceID)
        self.Hearing = SpeakerTCPCommunicator(portNumber=PortNumber)

    def ConnectTo(self, IPAddress):
        self.Talking.ConnectTo(IPAddress, PortNumber)

    def ConnectToConference(self, ConferenceIP, ConferencePortNo):
        self.Talking.ConnectToMultiCastGroup(ConferenceIP, ConferencePortNo)
        self.Hearing.JointMulticastGroup(ConferenceIP, ConferencePortNo)

    def LeaveConference(self, ConferenceIP, ConferencePortNo):
        self.Hearing.LeaveMulticastGroup()
        self.Talking.LeaveMulticastGroup()

    def Disconnect(self):
        self.Talking.Disconnect()

    def __del__(self):
        self.Hearing.Disconnect()
        del self.Talking
        del self.Hearing


def caller(DialTo, micDeviceID=1):
    caller = PhoneTerminal(micDeviceID)
    caller.ConnectTo(DialTo)
    print("Hold on")
    while (caller.Hearing.ConnectionEstablished == False):
        print ".",
        sleep(1)
    print("Client has connected back. Now you can talk")
    caller.Talking.clearBuffer()
    while (True):
        try:
            x = 0
            sleep(1)
            if (caller.Talking.ConnectionEstablished == False or caller.Hearing.ConnectionEstablished == False):
                print("The client has dropped the call")
                break
        except KeyboardInterrupt:
            break

    caller.Disconnect()


def GroupCaller(DialTo, PortNo, micDeviceID=1):
    caller = PhoneTerminal(micDeviceID)
    if (True):
        # try:
        caller.ConnectToConference(DialTo, PortNo)
        print("Hold on")
        while (caller.Hearing.ConnectionEstablished == False):
            print ".",
            sleep(1)
        print("Client has connected back. Now you can talk")

        while (True):
            try:
                x = 0
                sleep(1)
                if (caller.Talking.ConnectionEstablished == False or caller.Hearing.ConnectionEstablished == False):
                    print("The client has dropped the call")
                    break
            except KeyboardInterrupt:
                break
    # except Exception as e:
    #    print(e)

    caller.LeaveConference(DialTo, PortNo)


def reciever(micDeviceID=0):
    caller = PhoneTerminal(micDeviceID)

    while (True):
        try:
            x = 0
            sleep(1)
            if (caller.Hearing.ConnectionEstablished == True):
                print("The client " + str(caller.Hearing.callerIP[0]) + " has just connected..")
                caller.ConnectTo(caller.Hearing.callerIP[0])
                break
        except KeyboardInterrupt:
            break

    while (True):
        try:
            x = 0
            sleep(1)
            if (caller.Talking.ConnectionEstablished == False or caller.Hearing.ConnectionEstablished == False):
                print("The client has dropped the call")
                break
        except KeyboardInterrupt:
            break

    caller.Disconnect()


if __name__ == "__main__":

    MicTCPCommunicator.printListOfMicDevices()
    micDeviceID = 0
    areYouCaller = True
    isGroupCall = False

    if (isGroupCall):
        GroupCaller(MultiCastGrp, MuliCastPortNo, micDeviceID=micDeviceID)
    else:
        if (areYouCaller):
            caller(DialTo='172.16.63.36', micDeviceID=micDeviceID)

        else:
            reciever(micDeviceID=micDeviceID)