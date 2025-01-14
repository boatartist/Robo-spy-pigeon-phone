from gpiozero import AngularServo
from time import sleep



class Servo:
    def __init__(self, pin):
        self.servo = AngularServo(pin, min_pulse_width=0.0006, max_pulse_width=0.0023)
        self.angle = 0
        self.servo.angle = self.angle
    def correct_angle(self, angle):
        if -90 <= self.angle-angle <= 90: 
            self.angle = self.angle-angle
        elif self.angle-angle < -90:
            self.angle = -90
        else:
            self.angle = 90
