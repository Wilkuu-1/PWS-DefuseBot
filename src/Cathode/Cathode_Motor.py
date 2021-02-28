
#Python imports

#RPI imports
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class Motor():
    pin1 = None
    pin2 = None
    pin3 = None
    pwm  = None
    def __init__(self,pin1,pin2,pinpwm):
        self.pin1  = pin1
        self.pin2  = pin2
        GPIO.setup(pin1,  GPIO.OUT)
        GPIO.setup(pin2,  GPIO.OUT)
        GPIO.setup(pinpwm,GPIO.OUT)
        self.pwm = GPIO.PWM(pinpwm,50.0)

    def setSpeed(speed):
        if speed   < 0.001 and speed > -0.001:
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.HIGH) #BRAKE  (1 on  2 on)
        elif speed < -0.001:
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.HIGH) #BACK   (1 off 2 on)
        elif speed > 0.001:
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.LOW)  #FORWARD(1 on  2 off)
        self.pwm.ChangeDutyCycle(speed*100.0)
