#!/usr/bin/env python
#----------------------------------------------------------------------------
# Anode_Server module 
# Only to be invoked once 
# Hosts TCP server for Anode
#----------------------------------------------------------------------------
import socket
import sys
import math
import numpy as np
import time
import threading
from PIL import Image

#Socket Setup ---- Has to be the same on CATHODE
ADDR = ("127.0.0.1",21122) #Server adress 
HEAD = 2 #length of the msg_len message in bytes
#(2 bytes >> 65536 (Maximal recommended packet length for socket))
MAX = 65536 #Max package length
SOCK = socket.socket()

#Lingering socket fix (Server only)
SOCK.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#Connections
conns = []
outarray = np.ndarray((1000,1000,3)) #A way for the image to be fetched by Anode_GUI 
#Used to output to Anode_Server.outarray
def b2var(shape,byt):
    global outarray
    #Remake np array (read bytes + reshape)
    outarray = np.frombuffer(byt,dtype=np.uint8).reshape(shape)

def handle(conn,addr):
    print(f"[{addr}] Connected")
    msg_len = 4
    #While connected (msg_len bigger than head)
    while msg_len >= HEAD:
        msg_len = 0
        #Recieving list
        rec = []
        #image info gathering
        imcorrect = True 
        while True:
            msgl = conn.recv(HEAD)
            #break when message blank 
            if not msgl:
                imcorrect = False
                break
            msg_len = int.from_bytes(msgl,byteorder='big',signed=False)
            print(f"[{addr}] Recieved packet ({msg_len}b)")
            #When rec is 3 long extend rec[3] with recived packets
            if len(rec)>2:
                rec[2] = b''.join([rec[2],conn.recv(msg_len)])
                #if msg_len is less than MAX, finalize
                if msg_len < MAX:
                    print(f"[{addr}] Recieved image ({len(coll[2])}b)")
                    break
            else: #before that fill rec
                rec.append(conn.recv(msg_len))
        if imcorrect: #Now the image will be saved if correct
            #uint_64 -> int conversion
            rec[0] = int.from_bytes(rec[0],byteorder='big',signed=False)
            rec[1] = int.from_bytes(rec[1],byteorder='big',signed=False)
            #Shape tuple
            shap = (rec[0],rec[1],3)
            #Output 
            b2var(shap,rec[2])
    #close when the message length is too short 
    conn.close()

#Listening wrapper
def listen():
    while True:
        #Accept client
        conn,addr= sock.accept()
        #Handle only one client at the time 
        conns.append((conn,addr))
        handle(conn,addr)
        conns.remove((conn,addr))

#sends packet to CATHODE
def sender(byt,conn = conns[0]):
    #Size of byt
    leng = len(byt)
    if leng > MAX:
        #package splitting recursion
        print("[WARNING] CATHODE does not support transfers larger than {MAX}b,\n [WARNING] Sending in pieces anyway...")
        sender(byt[:MAX]) #sends first MAX bytes
        time.sleep(0.005)
        sender(byt[MAX:]) #sends the rest of the bytes
    else:
        #length in byte size 
        lenb.to_bytes(MAX,byteorder = 'big')
        print(f"[Sending] Packet with length {leng}")
        SOCK.send(lenb) #send length
        SOCK.send(pack) #send actual bytes

def start():
    #Enabling socket
    SOCK.bind(ADDR)
    SOCK.listen()
    #Activating listener
    lis = threading.Thread(function=listen)
    lis.start()
    print(f"[SERVER] ON AND LISTENING| ADDR {ADDR}")

