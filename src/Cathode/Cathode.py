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
import PIL
import io

#Own libs
import ANCA_Connect as ANODE
import Cathode_Motor

#RPI libs
from picamera import PiCamera
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

#Camera objects
camera = PiCamera()
#Kill var
notStopped = True

def givestatus(message):
    ANODE.SND(SOCK,message.encode('utf-8'),2)

def getkey(key):
    return keyval[keylist[key]]

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
    return speed, s != speed

def servoAngle(a,keyp,incr,CONT=False): #continous servo config 
    angle = a
    UP = getkey(f'{keyp}UP')
    DW = getkey(f'{keyp}DW')
    if   UP and not DW: angle= angle + incr
    elif DW and not UP: angle= angle - incr
    elif CONT : a = 0  
    if a > 1.0: a = 1.0
    if a < 0.0: a = 0.0
    return angle, angle != a

motorIncr = 0.2
servoIncr = [0.1,0.1,0.1,0.1]

def update():
    #init motors
    motorLSpeed = 0.0
    motorRSpeed = 0.0
    motorL = Cathode_Motor.Motor(27,22,12)
    motorR = Cathode_Motor.Motor(23,24,13)
    #init servos
    SERVO.set_pwm_freq(50) #Sets pwm freq to 60hz
    for i in range(9,12): #resets all servos to 0 position
        SERVO.setpwm(i,0,0)
    angles = [0.0,0.0,0.0,0.0]
    givestatus("update loop starting")
    #Loop
    while notStopped:
        motorLSpeed,Lch= motorSpeed(motorLSpeed,'RI','LE',motorIncr)
        motorRSpeed,Rch= motorSpeed(motorRSpeed,'LE','RI',motorIncr)
        if Lch: motorL.setSpeed(motorLspeed)
        if Rch: motorR.setSpeed(motorRspeed)
        angles[0],chS = servoAngle(angles[0],'A',servoIncr[0],CONT=True)
        if chS: SERVO.set_pwm(8,0,angles[0]*30+380)
        angles[1],chS = servoAngle(angles[1],'B',servoIncr[1],CONT=True)
        if chS: SERVO.set_pwm(9,0,angles[1]*30+380)
        angles[2],chS = servoAngle(angles[2],'C',servoIncr[2],CONT=True)
        if chS: SERVO.set_pwm(10,0,angles[2]*30+380)
        angles[3],chS = servoAngle(angles[3],'D',servoIncr[3])
        if chS: SERVO.set_pwm(11,0,angles[3]*50+375) #TODO Need to calibrate 

def keyset(byt,m):
    #TODO add some sync
    givestatus("a key has been set")
    key = int.from_bytes(byt,order='big',signed=False)
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

def handle():
    givestatus("handle loop starting")
    while True:
         func=print
         args=("blankfunc")
         toeval,pac = ANODE.REC(SOCK,funclink=CAfunc)
         for e in toeval:
            eval(e)
         func(*args)
    notStopped = False

#image buffer
imgbytes = io.BytesIO()

def picture():
    time.sleep(5) #camera warmup
    #take, parse, send: picture
    while notStopped:
        Camera.capture(imgbytes,"jpeg")
        ANODE.SND(SOCK,imgbytes.getvalue(),0) #sends pic as jpeg
        time.sleep(1/30) #simple refresh rate limiter

#Thread objects
picThread     = threading.Thread(target=picture)
manThread     = threading.Thread(target=update)

def start():
    #socket setup
    SOCK.connect(ANODE.AADDR)
    givestatus("connected")
    #3 loops:
    picThread.start() #sends pictures to Anode
    manThread.start()   #Manages the machine
    handle() #handles requests

if __name__ == "__main__":
    print(f"Cathode remote control client {version}:\n")
    start()

