import offline_tts
import display
from check_for_internet import *
import time
from wifi import *
from stt import get_speech
from picamera import PiCamera
from io import BytesIO
from PIL import Image, ImageDraw
import weather
from datetime import datetime

class Bird:
    wifi_modes = ['wifi', 'sim', 'none']
    non_existent_modes = ['texts']
    path = os.path.dirname(__file__) + '/'
    def __init__(self):
        self.Display = display.Display()
        self.Display.switch_mode(1)
        self.Display.main_menu()
        self.in_menu = False
        self.mode = None
        self.speaker = True
        self.has_internet = check_for_internet()
        self.wifi_mode = 'wifi'
        modem_off()
        wifi_on()
        self.prev_x, self.prev_y = 0, 0
        self.x, self.y = 0, 0
        self.has_new_input = False
        self.camera = PiCamera()
        self.camera.resolution = (240, 240)
        self.camera_stream = BytesIO()
        self.is_streaming = False
        self.note = []
        self.note_mode = 'menu'
        self.is_startup = True
        self.weather_info = ['No weather data', '']
        now = datetime.now()
        self.weather_time = int(now.strftime('%H%M'))
        self.now = now.strftime("%H:%M %d/%m/%Y")
        
    def home_page(self):
        now = datetime.now()
        current_time = int(now.strftime('%H%M'))
        self.now = now.strftime("%H:%M %d/%m/%Y")
        if current_time - self.weather_time >= 5 or self.is_startup:
            weather_info = weather.get_weather()
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
                offline_tts.speak('Notes', self.speaker)
                self.in_menu = False
                self.mode = 'notes'
                self.note = []
                self.note_mode = 'menu'
            elif self.x > 120 and self.y < 120:
                print('settings')
                offline_tts.speak('Settings', self.speaker)
                self.in_menu = False
                self.mode = 'settings'
                self.has_internet = check_for_internet()
            elif self.x < 120 and self.y > 120:
                print('camera')
                offline_tts.speak('Camera', self.speaker)
                self.in_menu = False
                self.mode = 'camera'
            else:
                print('sms')
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
            self.camera.start_preview()
            self.is_streaming = True
        self.camera_stream = BytesIO()
        self.camera.capture(self.camera_stream, format='jpeg')
        self.camera_stream.seek(0)
        img = Image.open(self.camera_stream)
        self.Display.camera_stream(img)
        if self.has_new_input:
            self.camera.capture(f'{Bird.path}final.jpg')
            self.camera.stop_preview()
            self.is_streaming = False
            self.mode = None
            self.in_menu = True
            self.Display.image = Image.new('RGB', (240, 240), 'WHITE')
            self.Display.draw = ImageDraw.Draw(self.Display.image)
    
    def note_menu(self):
        self.Display.notes_menu()
        if self.has_new_input:
            if self.x < 120 and self.y < 120:
                self.note_mode = 'view'
            elif self.x > 120 and self.y < 120:
                self.note_mode = 'text'
                self.note = []
            elif self.x < 120 and self.y > 120:
                self.note_mode = 'draw'
                self.drawing = []
            else:
                self.mode = None
                self.in_menu = True
    
    def text_notes(self):
        self.Display.text_notes(self.note)
        if self.has_new_input:
            if self.x <= 24:
                self.note = []
                self.note_mode = 'menu'
            elif self.x >= 216:
                self.Display.write('Transcribing...', (26, 116))
                self.Display.update()
                text = get_speech()
                length = 16
                self.note = [text[0+i:length+i] for i in range(0, len(text), length)]
            elif self.y >= 216:
                with open(f'{Bird.path}note.txt', 'a') as f:
                    f.write(''.join(self.note))
    
    def draw_notes(self):
        self.Display.draw_notes(self.drawing)
        if self.has_new_input:
            if 30 <= self.x <= 210 and 30 <= self.y <= 210:
                self.drawing.append((self.x, self.y))
            #exit
            elif self.x <= 24:
                self.drawing = []
                self.note_mode = 'menu'
            #new
            elif self.x >= 216:
                self.drawing = []
            #save
            elif self.y >= 216:
                files = os.listdir()
                nums = []
                for i in files:
                    if 'drawing' in i:
                        nums.append(int(i[7]))
                nums.sort()
                if len(nums) == 0:
                    num = 0
                elif len(nums) >= 4:
                    num = 0
                else:
                    num = nums[-1] + 1
                self.Display.write(f"Saving as drawing{num}.png", (4, 120))
                self.Display.update()
                pic = Image.new('RGB', (240, 240), 'WHITE')
                draw = ImageDraw.Draw(pic)
                prev = (0, 0)
                for pos in self.drawing:
                    draw.line((prev, pos), width=2, fill='black')
                    prev = pos
                pic.save(f'{Bird.path}drawing{num}.png')
                time.sleep(2)
    
    def view_notes(self):
        files = os.listdir()
        nums = []
        for i in files:
            if 'drawing' in i:
                nums.append(int(i[7]))
        self.Display.show_notes(len(nums))
        if self.has_new_input:
            self.note_mode = 'menu'
    
    def update(self):
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
                if self.note_mode == 'menu':
                    self.note_menu()
                elif self.note_mode == 'text':
                    self.text_notes()
                elif self.note_mode == 'draw':
                    self.draw_notes()
                elif self.note_mode == 'view':
                    self.view_notes()
     
        else:
            self.home_page()
        
        self.Display.update()
        self.prev_x, self.prev_y = self.x, self.y
        time.sleep(0.001)

if __name__ == '__main__':
    bird = Bird()
    while True:
        bird.update()