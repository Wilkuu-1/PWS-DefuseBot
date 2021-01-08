import socket
import cv2
import numpy as np
import time
from PIL import Image

#Server protocol info
DEST  =("127.0.0.1",21122)
SOCK  = socket.socket()
MAX   = 32768
#Video 
CAP = cv2.VideoCapture(0)


#Leave and send message
def close(msg):
    sendpack(msg)
    #Checks for longer messages
    if len(msg)> 8:
        sendpack("")
#Overloaded to leave without message
def close():
    close("")

def sendpack(pack):
    leng= len(pack)
    #Packet split (will recurse, sending one 65536-long packet every time)
    if leng > MAX:
        sendpack(pack[:MAX])
        time.sleep(0.005)
        sendpack(pack[MAX:])
    else:
        lenb= leng.to_bytes(8, byteorder = 'big')
        print(f"[Sending]: Packet with length {leng}")
        SOCK.send(lenb)
        SOCK.send(pack)

##MAIN LOOP
def start():
    SOCK.connect(DEST)
    while True:
        ret, imgc = CAP.read()
        if ret:
            #converting img to RGB then to binary
            img = cv2.cvtColor(imgc, cv2.COLOR_BGR2RGB)
            alt = img.tobytes()

            #Sending image resolution
            sendpack(img.shape[0].to_bytes(8,byteorder = 'big'))
            sendpack(img.shape[1].to_bytes(8,byteorder = 'big'))

            #Actual sending of image
            sendpack(alt)
            #Trial inp
            #frombytes
            #inp = Image.frombytes('RGB',(img.shape[0],img.shape[1]),alt)
            #fromarray
            #a = np.frombuffer(alt,dtype=np.uint8)
            #b = a.reshape(img.shape)
            #inp = Image.fromarray(b,mode='RGB') 
            #inp.save("./testin.png")
            input()
            #Wait for reply
            #inp = sock.recvfrom(buffsize)
    SOCK.close()
start()
