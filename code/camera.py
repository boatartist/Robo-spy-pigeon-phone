from picamera2 import Picamera2, Preview
from io import BytesIO
from PIL import Image, ImageDraw
from datetime import datetime
import time
import os

class CameraApp:
    path = '/home/pi/Desktop/galah/'
    def __init__(self):
        self.camera = Picamera2()
        self.camera.resolution = (240, 240)
        self.camera_stream = BytesIO()
        self.is_streaming = False
        self.mode = 'menu'

    def update(self, display, x, y, has_new_input):
        if not self.mode:
            self.mode = 'menu'
            return False
        if self.mode == 'menu':
            display = self.menu(display, has_new_input, x, y)
        elif self.mode == 'photo':
            display = self.photo(display, has_new_input, x, y)
        elif self.mode == 'gallery':
            display = self.gallery(display, has_new_input, x, y)
        else:
            self.mode = 'menu'
        return display

    def menu(self, display, has_new_input, x, y):
        display.four_menu()
        display.write('Gallery', (4, 84))
        display.write('Video (crash)', (128, 84))
        display.write('Photo', (4, 122))
        display.write('Exit', (128, 122))
        if has_new_input:
            if x < 120 and y < 120:
                self.mode = 'gallery'
                self.images = None
            elif x > 120 and y < 120:
                self.mode = 'video'
                i = 0/0
            elif x < 120 and y > 120:
                self.mode = 'photo'
            else: #exit
                self.mode = None
        return display

    def photo(self, display, has_new_input, x, y):
        if not self.is_streaming:
            camera_config = self.camera.create_still_configuration(main={'size': (240,240)}, lores={'size': (240,240)}, display='lores')
            self.camera.configure(camera_config)
            self.camera.start_preview(Preview.NULL)
            self.camera.start()
            self.is_streaming = True
        self.camera_stream = BytesIO()
        self.camera.capture_file(self.camera_stream, format='jpeg')
        self.camera_stream.seek(0)
        img = Image.open(self.camera_stream)
        display.camera_stream(img)
        display.rectangle((80, 120, 160, 200), 'WHITE')
        display.rectangle((84, 124, 156, 196), 'GRAY')
        display.write('<-', (10, 10), 'WHITE')
        if has_new_input:
            if x < 100 and y < 100:
                self.mode = 'menu'
                self.is_streaming = False
                self.camera.stop_preview()
                self.camera.stop()
            elif 80 <= x <= 160 and 120 <= y <= 200:
                display.loading()
                time.sleep(2)
                now = datetime.now()
                timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
                self.camera.capture_file(f'{CameraApp.path}photos/{timestamp}.jpg')
        return display

    def gallery(self, display, has_new_input, x, y):
        if not self.images:
            self.images = os.listdir(f'{CameraApp.path}photos')
            self.location = 0
        self.location %= len(self.images)
        img = Image.open(f'{CameraApp.path}photos/{self.images[self.location]}').resize((192, 192))
        display.fill_colour()
        display.image.paste(img, (24, 24))
        display.write('<', (4, 100), 'black')
        display.write('>', (216, 100), 'black')
        display.write(self.images[self.location], (24, 210), 'black')
        display.write('exit', (60, 10), 'black')
        if has_new_input:
            if x < 24:
                self.location -= 1
            elif x > 216:
                self.location += 1
            elif y < 24:
                self.mode = 'menu'
        return display
