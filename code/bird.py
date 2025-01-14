import offline_tts
import display
from check_for_internet import *
import time
from wifi import *
from stt import get_speech
from picamera2 import Picamera2, Preview
from io import BytesIO
from PIL import Image, ImageDraw
import weather
from datetime import datetime
import notes
from accelerometer import ADXL345
import servo

class Bird:
    wifi_modes = ['wifi', 'sim', 'none']
    non_existent_modes = ['texts']
    path = '/home/pi/Desktop/galah/'
    def __init__(self):
        self.Display = display.Display()
        self.Display.switch_mode(1)
        self.Display.loading()
        self.in_menu = False
        self.mode = None
        self.speaker = True
        self.has_internet = check_for_internet()
        print('interwebs check done')
        self.wifi_mode = 'wifi'
        modem_off()
        wifi_on()
        self.prev_x, self.prev_y = 0, 0
        self.x, self.y = 0, 0
        self.has_new_input = False
        self.camera = Picamera2()
        self.camera.resolution = (240, 240)
        self.camera_stream = BytesIO()
        self.notes = notes.Notes()
        self.is_streaming = False
        self.is_startup = True
        self.weather_info = ['No weather data', '']
        now = datetime.now()
        print('got time')
        self.weather_time = int(now.strftime('%H%M'))
        self.now = now.strftime("%H:%M %d/%m/%Y")
        self.accelerometer = ADXL345()
        self.frame = 0
        self.servo1 = servo.Servo(21)
        
    def home_page(self):
        now = datetime.now()
        current_time = int(now.strftime('%H%M'))
        self.now = now.strftime("%H:%M %d/%m/%Y")
        if current_time - self.weather_time >= 5 or self.is_startup:
            print('starting startup checks')
            weather_info = weather.get_weather()
            print('got weather, finally')
            if weather_info:
                self.weather_info = [f'{weather_info[0]}°C', weather_info[1]]
            else:
                self.weather_info = ['No weather data','']
            self.is_startup = False
            self.weather_time = current_time
        self.Display.home_screen(weather_info = self.weather_info, time = self.now)
        if self.has_new_input:
            self.in_menu = True
    
    def main_menu(self):
        self.Display.main_menu()
        if self.has_new_input:
            if self.x < 120 and self.y < 120:
                print('notes')
                self.Display.loading()
                offline_tts.speak('Notes', self.speaker)
                self.in_menu = False
                self.mode = 'notes'
                self.note = []
                self.note_mode = 'menu'
            elif self.x > 120 and self.y < 120:
                print('settings')
                self.Display.loading()
                offline_tts.speak('Settings', self.speaker)
                self.in_menu = False
                self.mode = 'settings'
                self.has_internet = check_for_internet()
            elif self.x < 120 and self.y > 120:
                print('camera')
                self.Display.loading()
                offline_tts.speak('Camera', self.speaker)
                self.in_menu = False
                self.mode = 'camera'
            else:
                print('sms')
                self.Display.loading()
                offline_tts.speak('Texts', self.speaker)
                self.in_menu = False
                self.mode = 'texts'
    
    def settings(self):
        self.Display.settings(self.wifi_mode, self.has_internet, self.speaker)
        if self.has_new_input:
            if self.x < 120 and self.y < 120:
                self.wifi_mode = Bird.wifi_modes[(Bird.wifi_modes.index(self.wifi_mode)+1)%3]
                if self.wifi_mode == 'wifi':
                    modem_off()
                    wifi_on()
                elif self.wifi_mode == 'sim':
                    wifi_off()
                    modem_on()
                else:
                    wifi_off()
                    modem_off()
            elif self.x > 120 and self.y < 120:
                pass
            elif self.x < 120 and self.y > 120:
                self.speaker = not self.speaker
            else:
                self.mode = None
                self.in_menu = True
    
    def camera_app(self):
        if not self.is_streaming:
            self.camera.start_preview(Preview.QTGL)
            camera_config = self.camera.create_still_configuration(main={'size': (240, 240)}, lores={'size':(240,240)}, display='lores')
            self.camera.configure(camera_config)
            self.camera.start()
            self.is_streaming = True
        self.camera_stream = BytesIO()
        self.camera.capture_file(self.camera_stream, format='jpeg')
        self.camera_stream.seek(0)
        img = Image.open(self.camera_stream)
        self.Display.camera_stream(img)
        if self.has_new_input:
            now = datetime.now()
            timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
            self.camera.capture_file(f'{Bird.path}{timestamp}.jpg')
            self.camera.stop_preview()
            self.camera.stop()
            self.is_streaming = False
            self.mode = None
            self.in_menu = True
            self.Display.image = Image.new('RGB', (240, 240), 'WHITE')
            self.Display.draw = ImageDraw.Draw(self.Display.image)
    
    def update(self):
        if self.frame == 500:
            pitch, roll = self.accelerometer.get_tilt_angles()
            self.servo1.correct_angle(roll)
            print(f'leaning forward {round(roll, 2)}°, sideways {round(pitch, 2)}°')
            self.frame = 0
        self.has_new_input = True
        self.x, self.y = self.Display.get_input()
        if self.x == self.prev_x and self.y == self.prev_y:
            self.has_new_input = False
        elif self.x == 0:
            self.has_new_input = False
            
        if self.in_menu:
            self.main_menu()

        elif self.mode and not self.mode in Bird.non_existent_modes:
            if self.mode == 'settings':
                self.settings()
            elif self.mode == 'camera':
                self.camera_app()
            elif self.mode == 'notes':
                self.Display, self.mode, self.in_menu = self.notes.update(self.Display, self.has_new_input, self.x, self.y, self.prev_x, self.prev_y)
        else:
            self.home_page()
        
        self.Display.update()
        self.prev_x, self.prev_y = self.x, self.y
        time.sleep(0.001)
        self.frame += 1

if __name__ == '__main__':
    bird = Bird()
    while True:
        bird.update()