import socket
import cv2
import sys
import math
import numpy as np
import time
from PIL import Image

#Socket Setup 
ADDR=("127.0.0.1",21122)
HEAD = 8
FORMAT = 'utf-8'
SOCK  = socket.socket()
SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCK.bind(ADDR)

#Other defaults
outputtovar = True

#SAVE FILE AS
#USED TO OUTPUT OUT OF THREAD
global recimage
def tovar(shape,pbytes):
    #RECREATE NP ARRAY 
    a = np.frombuffer(pbytes,dtype=np.uint8)
    b = a.reshape(shape)
    #CONSTRUCT IMAGE 
    out = b.rot90()
    recimage = out

def save(shape,pbytes,fname):
    #RECREATE NP ARRAY 
    a = np.frombuffer(pbytes,dtype=np.uint8)
    b = a.reshape(shape)
    #CONSTRUCT IMAGE 
    out = Image.fromarray(b,mode='RGB')
    out = out.rotate(-90,expand=1)
    #out = Image.frombytes('RGB',(shape[0],shape[1]),pbytes)
    out.save(fname)

def handle(conn,addr):
    print(f"[{addr}]: Successfully connected\n[ACTIVE NOW]:[{threading.activeCount() -1}]")
    msg_len = 8
    #RECIEVING WHILE CONNECTED 
    while msg_len >= HEAD:
        msg_len = 0
        coll = []
        #COLLECTING IMAGE INFO
        imcorrect = True
        while True:
            msgl = conn.recv(HEAD)
            #breaks when message blank
            if not msgl:
                imcorrect = False
                break
            msg_len = int.from_bytes(msgl,byteorder='big', signed=False)
            print(f"[{addr}]:Recieved packet of length ({msg_len})")
            if len(coll)>2:
                coll[2] =b''.join([coll[2],conn.recv(msg_len)])
                if msg_len < 32768:
                    print(f'[{addr}]:{len(coll[2])} bytes has been recieved')
                    break
            else:
                coll.append(conn.recv(msg_len))
        if imcorrect:
            #saving image
            fname =f"./out_{addr}.png"
            #converting uint_64 to python int
            coll[0]= int.from_bytes(coll[0],byteorder='big', signed=False)
            coll[1]= int.from_bytes(coll[1],byteorder='big', signed=False)
            #creating shape tuple
            shap = (coll[0],coll[1],3)
            print(f"[addr]:Shape tuple of image array:{shap} ")
            #calling save function
            if outputtovar:
                tovar(shap,coll[2])
            save(shap,coll[2],fname)
    conn.close()

def start():
    SOCK.listen() #Socket is now listening
    print(f"[SERVER]:Listening @ | {ADDR} |.")
    while True:
        conn, addr = SOCK.accept()
        #the server will now allow only one client
        handle(conn,addr)
        #It used threads previously:
        #t = threading.Thread(function = handle)
        #t.start()




