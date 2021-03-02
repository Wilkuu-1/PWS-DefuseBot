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
from PIL import Image
import io

sigs = []
outimg = Image.fromarray(np.random.randint(0,255,(1000,1000,3)),mode="RGB") #Array for Anode_GUI
imgbuf = io.BytesIO()
outupdated = True

def b2var(byt): #creates array from bytes and sets outarray with it
    global outimg
    global outupdated
    #First 4 bytes define resolution (2 ints), 3 colors
    try: #array creation
        imgbuf.write(byt)
        outupdated = False
        outimg = Image.open(imgbuf)
        outupdated = True
    except:
        print("frame dropped")
def status(byt):
    print(f"Message from Cathode:\n{byt.decode(utf-8)}")

def signal(signal,func):
    sigs.append((signal,func))
    print(f"signal {signal} func: {func} sent")
#Request handler used as a interface for CATHODE
class REQ(ssv.BaseRequestHandler):
    def setup(self):
        print(f"Someone Connected")
    #function error function
    def ferr(nr):
        raise ValueError(f"[Error]Number [{nr}] not linked.")
    #handle function
    def handle(self):
        global sigs
        print(self.request.recv(0))
        while True:
            for x in range(2):
                fun,pac,func = CATH.REC(self.request,funclink=funcl) #recieves packet
                try:
                    exec(fun)
                    print(f"| {fun} |did execute")
                except:
                    print(f"| {fun} |did not execute")
            if not sigs: sigs = [("abcd",254)]
            CATH.SND(self.request,sigs[0]) #Send all signals from sigs list
            sigs = sigs[1:]
            #execs all from funclink
def start():#starts server
    with ssv.ThreadingTCPServer(AADDR,REQ) as ANODE:
        print(f"[SERVER]Listening on: {AADDR}")
        ANODE.serve_forever()
