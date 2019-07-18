# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 09:02:43 2019

@author: RayomandVatcha
"""
import usb.core
import usb.util
from time import sleep
import array

def getStringDescriptor(device, index):
    """
    """
    response = device.ctrl_transfer(usb.util.ENDPOINT_IN,
                                    usb.legacy.REQ_GET_DESCRIPTOR,
                                    (usb.util.DESC_TYPE_STRING << 8) | index,
                                    0, # language id
                                    255) # length

    # TODO: Refer to 'libusb_get_string_descriptor_ascii' for error handling
    
    return response[2:].tostring().decode('utf-16')

REQUEST_TYPE_SEND = usb.util.build_request_type(usb.util.CTRL_OUT,
                                                usb.util.CTRL_TYPE_CLASS,
                                                usb.util.CTRL_RECIPIENT_DEVICE)

REQUEST_TYPE_RECEIVE = usb.util.build_request_type(usb.util.CTRL_IN,
                                                usb.util.CTRL_TYPE_CLASS,
                                                usb.util.CTRL_RECIPIENT_DEVICE)

USBRQ_HID_GET_REPORT = 0x01
USBRQ_HID_SET_REPORT = 0x09
USB_HID_REPORT_TYPE_FEATURE = 0x03

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()




class PhysicalKey:
    
    def __init__(self, idVendor= 0x16c0, idProduct=0x05df):
        self.idVendor = idVendor
        self.idProduct = idProduct

        # TODO: Make more compliant by checking serial number also.
        print("[Info :] Attach the physical key")
        while(True):
            self.device = usb.core.find(idVendor=self.idVendor,
                                    idProduct=self.idProduct)

            if self.device is not None:
                break
            sleep(1)
            print ".",
        print("[Info :] The physical key is connected")
        
        sleep(0.1)
        jsonData = ""
        print(self.write([10]));
        
        StartStoring = False
        while(True):
                i = self.read()
                if(i is not None):
                    ct = chr(i)
                    print(ct)
                    if(ct == '{'):
                        StartStoring = True
                    if(StartStoring):
                        jsonData = jsonData + ct
                        if(ct=='d'):
                           break
                sleep(0.01)
        self.KeyDetails = jsonData
                
            
            
    def write(self, byte):
        """
        """
        # TODO: Return bytes written?
        #print "Write:"+str(byte)
        #self._transferW(REQUEST_TYPE_SEND, USBRQ_HID_SET_REPORT, 0, byte) # ignored
        #print(self._transfer(REQUEST_TYPE_SEND, USBRQ_HID_SET_REPORT, byte, [])) # ignored
        return self._transfer(REQUEST_TYPE_SEND, USBRQ_HID_SET_REPORT, 0, byte) # ignored            
        
        
    def read(self):
        """
        """
        response = self._transfer(REQUEST_TYPE_RECEIVE, USBRQ_HID_GET_REPORT,
                              0, # ignored
                              1) # length

        if not response:
            return None
        
        return response[0]
    

    def _transfer(self, request_type, request, index, value):
        """
        """
        return self.device.ctrl_transfer(request_type, request,
                                        (USB_HID_REPORT_TYPE_FEATURE << 8) | 0,
                                         index,
                                         value)

    def __del__(self):
        usb.util.release_interface(self.device, 0x81)
        
    def ReadKeyBoardStrokes(self):
        return _Getch()
        

import simplejson as json
class PersonProfile(PhysicalKey):
    
    def __init__(self):
        PhysicalKey.__init__(self)
        self.ProfileInformationObject = json.loads(self.KeyDetails)
        
    def getKey(self, ID):
        return self.ProfileInformationObject[0][ID]['PWD']
        
    
if __name__ == '__main__':
    pr = PersonProfile()
    print(pr.ProfileInformationObject)
    del pr
    