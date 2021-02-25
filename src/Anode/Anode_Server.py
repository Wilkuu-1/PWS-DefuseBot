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
from PIL import Image #Might not be necessary in the end

sigs = []
outarray = np.random.randint(0,255,(1000,1000,3)) #Array for Anode_GUI
def b2var(byt): #creates array from bytes and sets outarray with it
    global outarray
    #First 4 bytes define resolution (2 ints), 3 colors
    shap  = (int.from_bytes(byt[0:2],signed=False),
             int.from_bytes(byt[2:4],signed=False), 3)
    byt = byt[4:]
    try: #array creation
        outarray = np.frombuffer(byt,dtype=np.uint8).reshape(shap)
    except:
        print("frame dropped")

def signal(signal,func):
    sigs.append((signal,func))
    print(f"signal {signal} func: {func} sent")
#Request handler used as a interface for CATHODE
class REQ(ssv.BaseRequestHandler):
    def setup(self):
        conns.append(self.request)
        print(f"[{client_address}] Connected")
    #function error function
    def ferr(nr):
        raise ValueError(f"[Error]Number [{nr}] not linked.")
    #handle function
    def handle(self):
        while True:
            fun,pac,head = CATH.REC(self.request,funclink=funcl) #recieves packet
            if sigs:
                for sig in sigs:
                    CATH.SND(self.request,sig[0],sig[1]) #Send all signals from sigs list
            sigs = []
            args = ("[WARNING]Blank function eval call")
            func =  print
            for x in fun: #evals all from funclink
                eval(x)
            func(*args) #executes constructed function
            CATH.SND(self.request,b"abcd",1) #Acknowleges packet

def start():#starts server
    with ssv.ThreadingTCPServer(AADDR,REQ) as ANODE:
        print(f"[SERVER]Listening on: {AADDR}")
        ANODE.serve_forever()
