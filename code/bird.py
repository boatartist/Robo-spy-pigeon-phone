import offline_tts
import display
from check_for_internet import *
import time
from wifi import *

class Bird:
    wifi_modes = ['wifi', 'sim', 'none']
    non_existent_modes = ['texts', 'notes', 'camera']
    def __init__(self):
        self.Display = display.Display()
        self.Display.switch_mode(1)
        self.Display.main_menu()
        self.in_menu = True
        self.mode = None
        self.speaker = True
        self.speaking = True
        self.wifi_mode = 'wifi'
        modem_off()
        wifi_on()
        self.prev_x, self.prev_y = 0, 0
        self.x, self.y = 0, 0
        self.has_new_input = False
        
    def main_menu(self):
        self.Display.main_menu()
        if self.has_new_input:
            if self.x < 120 and self.y < 120:
                print('notes')
                offline_tts.speak('Notes', self.speaker)
                self.in_menu = False
                self.mode = 'notes'
            elif self.x > 120 and self.y < 120:
                print('settings')
                offline_tts.speak('Settings', self.speaker)
                self.in_menu = False
                self.mode = 'settings'
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
        self.Display.settings(self.wifi_mode, self.speaking, self.speaker)
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
                self.speaking = not self.speaking
            elif self.x < 120 and self.y > 120:
                self.speaker = not self.speaker
            else:
                self.mode = None
                self.in_menu = True
    
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
        else:
            self.mode = None
            self.in_menu = True
        
        self.Display.update()
        self.prev_x, self.prev_y = self.x, self.y
        time.sleep(0.001)

if __name__ == '__main__':
    bird = Bird()
    while True:
        bird.update()