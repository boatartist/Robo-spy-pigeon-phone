from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()

class Servo:
    def __init__(self, pin):
        self.servo = AngularServo(pin, pin_factory=factory) #, min_pulse_width=0.0006, max_pulse_width=0.0023)
        self.angle = 0
        self.servo.angle = self.angle
    def correct_angle(self, angle):
        if -90 <= angle <= 90: 
            self.angle = angle
        elif angle < -90:
            self.angle = -90
        else:
            self.angle = 90
