#!/bin/env python3
#
#------------------------------------------------------------------------------
# Cathode -
# Version V0.1
# Execute as side process on the on-board raspberry pi zero
#------------------------------------------------------------------------------
version = "V0.1"
f"Cathode remote control client {version}:\n"

#python libs
import math
import time
import socket
import threading

#Connect lib
import ../ANCA_Connect.py as ANODE

#RPI libs


#Global socket
SOCK = socket.socket()
#Funclink choice
Flnk = ANODE.CAfunc

#key dict
keylst={'UP':25,
        'DW':39,
        'LE':38,
        'RI':40,
        'AUP':79,
        'ADW':83,
        'BUP':80,
        'BDW':84,
        'CUP':81,
        'CDW':85,
        'DUP':88,
        'DDW':87}

keyval ={25:False,
         38:False,
         39:False,
         40:False,
         79:False,
         81:False,
         81:False,
         83:False,
         84:False,
         85:False,
         87:False,
         88:False}

def update():
    #RPI motor control stuff here

def keyset(byt,m):
    #TODO add some sync
    key = int.from_bytes(byt,order='big',signed=False)
    if m > 1: #check if the key has to be toggled
        keyval[key] = !keyval[key]
    else:
        keyval[key]=bool(m))

def setstatus(byt): #dangerous value changing function
    t = int(byt[0])
    name = byt[1:9].decode('utf-8')
    valb = byt[8:]
    if t == 0:
        eval(f"{name}={bool(valb)}")
    if t == 1:
        eval(f"{name}={int(valb)}")
    if t == 2:
        eval(f"{name}={string(valb)}")

def handle():
    while True:
         func=print
         args=("blankfunc")
         toeval,pac = ANODE.REC(SOCK,funclink=CAfunc)
         for e in toeval:
            eval(e)
         func(*args)

def picture():
    #take, parse, send: picture
    #RPI Stuffs

def start():
    #socket setup
    SOCK.connect(ANODE.AADDR)
    #3 loops:
    #the first handles requests from anode
    #the second sends image data and other thing
    #the third manages the machine


if __name__ == "__main__":
    print(f"Cathode remote control client {version}:\n")
    start()
