#!/usr/bin/env python
#
#-----------------------------------------------------------------------------#
# Anode_Server module V1.1
# Only to be called and use once at the time
# Responsible for communications between Anode and Cathode
#-----------------------------------------------------------------------------#
#Connect library
import ANCA_Connect as CATH
funcl = CATH.ANfunc
AADDR = CATH.AADDR
#Important imports
import socketserver as ssv
import numpy as np
import threading
#QOL imports
import sys
import math
import time
from PIL import Image,ImageFile
import io


class byteImage(): #Data type that includes the buffer in which the image is stored TODO get this class its own place
    def __init__(self):
        self.Storage = io.BytesIO()
        Image.fromarray(np.random.randint(0,255,(640,480,3),np.uint8),mode="RGB").save(self.Storage,format='jpeg')
        self.Image = Image.open(self.Storage)
        self.updated = True
    def mkimg(self,byt):
        self.Updated = False
        self.Storage.seek(0)
        self.Storage.truncate(0)
        self.Storage.write(byt)
        self.Image = Image.open(self.Storage)
        self.Updated = True
    def getimg(self): #anode
        self.Updated = False
        return self.Image
    def dumpimg(self):
        return self.Storage.getvalue()


outimage = byteImage() #inits the image that

def b2var(byt): #wrapper for changing the image of outimage
    try: #Image object creation
        outupdated = False         #redundant disabling of flag
        outimage.mkimg(byt)     #opens image
        outupdated = True          #enable flag when done
    except Exception as e:
        print(f"Frame dropped:{e}")

def status(byt):
    print(f"Cathode: {byt.decode('utf-8')}")

def signal(signal,func):
    sigs.append((signal,func))
    print(f"Sent: signal {signal} func: {func}")

#Request handler used as a interface for CATHODE
class REQ(ssv.BaseRequestHandler):
    def setup(self):
        print(f"Device Connected")
    #function error function
    def ferr(self,nr):
        raise ValueError(f"[Error]Number [{nr}] not linked.")
    #handle function
    def handle(self):
        global sigs
        print(self.request.recv(0))
        while True:
            fun,pac,func = CATH.REC(self.request,funclink=funcl) #recieves packet
            try:
                exec(fun)
            except Exception as e:
                print(f"| {fun} |did not execute: {e}")
            if not sigs: sigs = [(b"abcd",0)]
            CATH.SND(self.request,*sigs[0]) #Send all signals from sigs list
            sigs = sigs[1:]
sigs = [(b"abcd",0)]
            #execs all from funclink
def start():#starts server
    with ssv.ThreadingTCPServer(AADDR,REQ,bind_and_activate=False) as ANODE:
        ANODE.allow_reuse_address = True
        ANODE.server_bind()
        ANODE.server_activate()
        print(f"[SERVER]Listening on: {AADDR}")
        ANODE.serve_forever()
