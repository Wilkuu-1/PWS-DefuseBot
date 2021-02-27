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
import ../ANCA_Connect.py as ANODE
import ./Cathode_Motor

#RPI libs
from picamera import PiCamera
import smbus
import Adafruit_PCA9685
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

#Thread objects
picThread     = Threading.Thread(target=picture)
handleThread  = Threading.Thread(target=handle)
manThread     = Threading.Thread(target=update)
#Camera objects
camera = PiCamera()

def getkey(key)
    return keyval[keylist[key]]

def motorSpeed(s,key,antag,incr): #TODO tune and test all key combos
    UP = getkey('UP') #Probe controls
    DW = getkey('DW')
    KE = getkey(key)
    AN = getkey(antag)
    speed = s
    if speed < 1.0:
        if UP and !DW: speed=speed+incr #Forward increase
        if KE:         speed=speed+incr #Turn increase
    if speed > -1.0:
        if DW and !UP:
            speed=speed-incr #Backward decrease
            if speed >0.0  :speed=0 #Stop if want to go backwards
        elif speed > 0.5  and AN and UP :speed=0.5 #Cap speed going forward and turning other way
        if AN: speed=speed-incr #Turn decrease
    if   speed > 1.0 : speed = 1.0 #clamp
    elif speed < -1.0: speed = -1.0
    return speed, s != speed

def servoAngle(a,keyp,incr):
    angle = a
    UP = getkey(f'{keyp}UP')
    DW = getkey(f'{keyp}DW')
    if   UP and !DW: angle= angle + incr
    elif DW and !UP: angle= angle - incr
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
    angles = [0.0,0.0,0.0,0.0]
    #Loop
    while True:
        motorLSpeed,Lch= motorSpeed(motorLSpeed,'RI','LE',motorIncr)
        motorRSpeed,Rch= motorSpeed(motorRSpeed,'LE','RI',motorIncr)
        if Lch: motorL.setSpeed(motorLspeed)
        if Rch: motorR.setSpeed(motorRspeed)
        angles[0],chS = servoAngle(angles[0],'A',servoIncr[0])
        if chS: Servo.someServoFunction(angles[0])
        angles[1],chS = servoAngle(angles[1],'B',servoIncr[1])
        if chS: servos[1].someServoFunction(angles[1])
        angles[2],chS = servoAngle(angles[2],'C',servoIncr[2])
        if chS: servos[2].someServoFunction(angles[2])
        angles[3],chS = servoAngle(angles[3],'D',servoIncr[3])
        if chS: servos[3].someServoFunction(angles[3])

def keyset(byt,m):
    #TODO add some sync
    key = int.from_bytes(byt,order='big',signed=False)
    if m > 1: #check if the key has to be toggled
        keyval[key] = !keyval[key]
    else:
        keyval[key]=bool(m))

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

def handle():
    while True:
         func=print
         args=("blankfunc")
         toeval,pac = ANODE.REC(SOCK,funclink=CAfunc)
         for e in toeval:
            eval(e)
         func(*args)

#image buffer
imgbytes = io.BytesIO()

def picture():
    #take, parse, send: picture
    #PIL.Image: pic = someRPICamFunction
    pic.save(imgbytes,format="jpeg")
    ANODE.SND(SOCK,imgbytes.getvalue(),0) #sends pic as jpeg

def start():
    #socket setup
    SOCK.connect(ANODE.AADDR)
    #3 loops:
    picThread.start() #sends pictures to Anode
    handleThread.start() #handles requests from Anode
    manThread.start()   #Manages the machine

if __name__ == "__main__":
    print(f"Cathode remote control client {version}:\n")
    start()
