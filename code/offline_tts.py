from time import sleep
import os
from gpiozero import OutputDevice

speaker = OutputDevice(12)
speaker.off()
def speak(text='Hello World', speaker_on=True):
    if speaker_on:
        speaker.on()
    os.system(f'espeak "{text}" -s 120 -ven+f3 --stdout | aplay -D hw:1,0')
    speaker.off()
    
if __name__ == '__main__':
    speak('hello, i am a robot, running on a raspberry pi zero, i am not broken. Please, do not break.')
