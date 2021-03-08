#!/bin/env python3
#
#    This script will help you tune the servo's 
#
import math
import time 
from Adafruit_PCA9685 import PCA9685

pwm = PCA9685()
sep = "|---------------------------------------------------------------|"
dcintro   = "In this step you will have to reach the duty cycle at which:"
dcprompt = "Enter DC in % (float): 'stop' to end"
def setDC(percent,nservo):
    bit = int(40.96*percent)
    print(f"DC set to {percent}, ({bit}) ")
    pwm.set_pwm(nservo,0,bit)

def selectDC(num,Stop = None ):
    inp = ""
    previnp = ""
    while True:
        try:
            inp = input('>').strip()
            if inp == 'stop':
                if Stop: setDC(Stop,num) #stops the continous servo after choice
                return float(previnp)
            else:
                setDC(float(inp),num)
                previnp=inp       #saves the correct output before 'stop'
        except Exception as e:
            print(f"Try inputting again ({e})")

def continousservo(num):
    #dutycycle at which the servo stops
    print(dcintro)
    print("The servo stops. \n There will be a region at which this occurs.")
    print("Pick the middle")
    time.sleep(2)
    print(dcprompt)
    stop = selectDC(num)
    print(f"The middle of the duty cycle region at which the servo stops is: {stop}% ")
    loop = True
    print(sep)
    print(dcintro)
    print("At which the servo reaches the desired speed")
    print("We only need to do this once as the speeds should be symmetrical from the middle(stop).")
    time.sleep(2)
    print(dcprompt)
    maxi = selectDC(num,Stop = stop)
    if maxi > stop: 
        mini = stop-(maxi-stop)
    else:
        mini = maxi
        maxi = stop+(stop-mini)
    print(sep)
    print("Results (Please save them before continuing):")
    print(f"Full CW: {mini},Stop: {stop}, Full CCW: {maxi}")
    print("[-1]--------------[0]-------------------[+1]")
    input("Press any key to continue:")

def standardservo(num):
    print("this mode will be implemented later")
    print("Press any key to continue:")

def servotune(): #prompting funtion 
    print("Choose servo mode:")
    continous = None #Continous?
    num       = 0    #Number?
    loop = True
    while loop: #Infinetly asks till satisfactory result recieved 
        try:
            continous = bool(int(input("Standard (0), Continuous (1+)")))
            loop = False 
        except:
            print("Try again")
    loop = True
    while loop: #Same here
        try:
            num = int(input("Enter the connection number between 0 and 15"))
            if num < 0 or num > 15: raise ValueError("") #dummy error
            loop = False
        except: 
            print("Try again")
    print(sep)
    if continous:
        continousservo(num)
    else: 
        standardservo(num)
    return "Y" == input("repeat with other servo? (Y/)").upper()


print("Servo tune program for continuous servo's and standard servo's\n" + sep)
while servotune():
    print(sep)
    time.sleep(1)

