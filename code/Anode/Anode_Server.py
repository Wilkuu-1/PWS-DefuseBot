#


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
ADDR = ("127.0.0.1",21122)
HEAD = 4 #length of the msg_len message

SOCK = socket.socket()
#Lingering socket fix
SOCK.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#Connections
conns = []
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
            b2var(shap,rec[2]):
    #close when the message length is too short 
    conn.close()

#Listening wrapper
def listen():
    while True:
        #Accept client
        conn,addr= sock.accept()
        #Handle only one client
        conns.append((conn,addr))
        handle(conn,addr)
        conns.remove((conn,addr))

#sends packet to CATHODE #TODO
def sender(byt,conn = conns[0]):
    pass

def start():
    #Enabling socket
    SOCK.bind(ADDR)
    SOCK.listen()
    #Activating listener
    lis = threading.Thread(function=listen)
    lis.start()
    print(f"[SERVER] ON AND LISTENING| ADDR {ADDR}")

