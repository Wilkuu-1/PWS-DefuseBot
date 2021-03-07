#!/bin/env python3
#
#------------------------------------------------------------------------------
# Cathode -
# Version V0.1
# Execute as side process on the on-board raspberry pi zero
#------------------------------------------------------------------------------
version = "V0.1"
f"Cathode remote control client {version}:\n"

framerate = 30 
execdelay = 0.02

#python libs
import math
import time
import socket
import threading
import PIL
from io import BytesIO

#Own libs
import ANCA_Connect as ANODE
import Cathode_Motor

#RPI libs
from picamera import PiCamera, PiCameraCircularIO
import Adafruit_PCA9685
import smbus
import RPi.GPIO as GPIO

#GPIO Convention
GPIO.setmode(GPIO.BCM)
#Servo controller
SERVO = Adafruit_PCA9685.PCA9685()
#Global socket
SOCK = socket.socket()
#Funclink choice
Flnk = ANODE.CAfunc
#key dict (setting controls)
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
#Keys pressed or not pressed
keyval ={keylst['UP']:False,
         keylst['LE']:False,
         keylst['DW']:False,
         keylst['RI']:False,
         keylst['AUP']:False,
         keylst['ADW']:False,
         keylst['BUP']:False,
         keylst['BDW']:False,
         keylst['CUP']:False,
         keylst['CDW']:False,
         keylst['DUP']:False,
         keylst['DDW']:False}

#signals var
sigs=[("Cathode: Hello".encode('utf-8'),2)]
#kill var
def setStopped(b):
    global notStopped
    notStopped = b 

def givestatus(message):
    if len(sigs) < 5:
        sigs.append((message.encode('utf-8'),2))

def getkey(key):
    return keyval[keylst[key]]

def motorSpeed(s,key,antag,incr): #TODO tune and test all key combos
    UP = getkey('UP') #Probe controls
    DW = getkey('DW')
    KE = getkey(key)
    AN = getkey(antag)
    speed = s
    if speed < 1.0:
        if UP and not DW: speed=speed+incr #Forward increase
        if KE:         speed=speed+incr #Turn increase
    if speed > -1.0:
        if DW and not UP and not KE:
            speed=speed-incr #Backward decrease
            if speed >0.0 and not KE :speed=0 #Stop if want to go backwards
        elif speed > 0.5  and AN and UP :speed=0.5 #Cap speed going forward and turning other way
        if AN: speed=speed-incr #Turn decrease
    if speed != 0 and not UP and not DW and not AN and not KE: speed = 0
    if   speed > 1.0 : speed = 1.0 #clamp
    elif speed < -1.0: speed = -1.0
    return speed 

def servoAngle(a,keyp,incr,CONT=False): #continous servo config 
    angle = a
    UP = getkey(f'{keyp}UP')
    DW = getkey(f'{keyp}DW')
    if   UP and not DW: angle= angle + incr
    elif DW and not UP: angle= angle - incr
    elif CONT : a = 0  
    if a > 1.0: a = 1.0
    if a < 0.0: a = 0.0
    return angle

motorIncr = 0.2
servoIncr = [0.1,0.1,0.1,0.1]

def update():
    #init motors
    motorL = Cathode_Motor.Motor(27,22,12)
    motorR = Cathode_Motor.Motor(23,24,13)
    motorLSpeed = 0.0
    motorRSpeed = 0.0
    #init servos
    SERVO.set_pwm_freq(50) #Sets pwm freq to 60hz
    angles = [0.0,0.0,0.0,0.0]
    givestatus("update loop starting")
    #Loop
    while notStopped:
        motorLSpeed = motorSpeed(motorLSpeed,'RI','LE',motorIncr)
        motorRSpeed = motorSpeed(motorRSpeed,'LE','RI',motorIncr)
        motorL.setSpeed(motorLSpeed)
        motorR.setSpeed(motorRSpeed)
        angles[0] = servoAngle(angles[0],'A',servoIncr[0],CONT=True)
        SERVO.set_pwm(8,0,int(angles[0]*30+380))
        angles[1] = servoAngle(angles[1],'B',servoIncr[1],CONT=True)
        SERVO.set_pwm(9,0,int(angles[1]*30+380))
        angles[2] = servoAngle(angles[2],'C',servoIncr[2],CONT=True)
        SERVO.set_pwm(10,0,int(angles[2]*30+380))
        angles[3] = servoAngle(angles[3],'D',servoIncr[3])
        SERVO.set_pwm(11,0,int(angles[3]*50+375)) #TODO Need to calibrate 
    angles = [0.0,0.0,0.0,0.0]
    for i in range(0,2):
        SERVO.set_pwm(8+1,0,int(angles[i]*30+380))
    SERVO.set_pwm(8+1,0,int(angles[3]))

def keyset(byt,m):
    #TODO add some sync
    givestatus("a key has been set")
    key = int.from_bytes(byt,byteorder='big',signed=False)
    if m > 1: #check if the key has to be toggled
        keyval[key] = not keyval[key]
    else:
        keyval[key]=bool(m)

def setstatus(byt): #dangerous value changing function
    t = int.from_bytes(byt[0],byteorder='big',signed=False)
    name = byt[1:9].decode('utf-8')
    valb = byt[8:]
    if t == 0:
        eval(f"{name}={bool(valb)}")
    if t == 1:
        eval(f"{name}={int(valb)}")
    if t == 2:
        eval(f"{name}={string(valb)}")
    givestatus("variable {name} changed to {valb}")

def ferr():
    #print("invalid func")
    pass


camera = PiCamera(resolution=(640,480),framerate=60)
class byteImage():
    def __init__(self):
        self.Storage = BytesIO()
        self.ready   = False
    def update(self):
        self.ready = False
        self.Storage.seek(0)
        self.Storage.truncate(0)
        camera.capture(self.Storage,format='jpeg',use_video_port=True,quality=25) #Captures image as jpeg file into the stream
        self.ready = True
    def getdump(self):
        return self.Storage.getvalue()
    def setready(self,ready):
        self.ready = ready

img = byteImage() 

def picture(): #takes pictures @30fps max
    readready = False
    delay = 0.01
    time.sleep(3) #Camera warmup
    print("starting recording")
    print(notStopped)
    while notStopped:
        if not img.ready:       #Checks if previous frame had been sent
            img.update()
            sigs.append("img")      #Adds the "img" internal signal 
            time.sleep((1/framerate)-(execdelay+delay)) #TODO make this less lazy #Sets framerate using delay
        else:
            time.sleep(delay)
    camera.close()

def handle(): #handles communications with Anode
    global sigs
    time.sleep(1)
    print(notStopped)
    print('starting exchange of signals')
    while notStopped:
        #Sending part
        if sigs[0] != "img":        #Picks up the "img" internal signal
            ANODE.SND(SOCK,*sigs[0])            #Sends any other signal
        else:
            while not img.ready: pass           #Waits till an image is ready
            print("frame sending")
            ANODE.SND(SOCK,img.getdump(),0)  #Reads the entire buffer and sends it to Anode
            img.setready(False)
        sigs=sigs[1:]                     #Removes sent signal
        if len(sigs)<1: sigs.append(("ECHO".encode('utf-8'),1)) #Adds the idle signal if no signals are to be sent
        #Recievieng part
        toexec,pac,func = ANODE.REC(SOCK,funclink=ANODE.CAfunc)
        try: #Tries to execute the funclink
            exec(toexec) 
        except Exception as e:
            print(e)
            #givestatus(f"CATH: {toexec} not executed")


#Thread objects
manThread     = threading.Thread(target=update)
picThread     = threading.Thread(target=picture)
def start():
    #socket setup
    setStopped(True)
    SOCK.connect(ANODE.AADDR)
    givestatus("connected")
    #3 loops:
    picThread.start()   #takes pictures
    manThread.start()   #Manages the machine
    handle() #handles requests
    setStopped(False) #stop everything
    time.sleep(1) #Wait for other processes

if __name__ == "__main__":
    print(f"Cathode remote control client {version}:\n")
    start()

