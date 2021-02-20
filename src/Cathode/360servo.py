#Sets all servo's to 0
#Uses: PCA9685 board, Servo's: Futaba S3003, SG90 9g
#IO
from board import SDA,SCL
import busio
import time

#Servo module
from adafruit_motor   import servo
from adafruit_pca9685 import PCA9685

#I2C and Servo Object Init
I2C=busio.I2C(SCL,SDA)
SERVO=PCA9685(I2C)
SERVO.frequency = 50 #50Hz

#Creates servo objects, (Adjust pulse widths till satisfied)
servos = [servo.Servo(chan,min_pulse=1520,max_pulse=1900) for chan in SERVO.channels ]
c = 0 
for servo in servos:
    for a in range(1,180):
        servo.angle = a
    for b in range(0,179,-1):
        servo.angle = b
    print(f"Servo {c} moved.")
    c=c+1

input("Servo's moved, Press any key to close")
