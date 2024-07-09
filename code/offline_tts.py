from time import sleep
import os
import pygame

def speak(text='Hello World'):
    os.system(f'espeak "{text}" -s 120 -ven+f3 --stdout | aplay -D hw:2,0')
    sleep(1)
    
if __name__ == '__main__':
    speak()