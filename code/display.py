import time
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont
from lib import LCD_1inch28, Touch_1inch28

class Display:
    def __init__(self, bg_colour='WHITE', font_name='Font00', font_size=24, mode=0):
        self.mode = mode
        self.bg_colour = bg_colour
        self.touch = Touch_1inch28.Touch_1inch28()
        self.disp = LCD_1inch28.LCD_1inch28()
        self.disp.Init()
        self.touch.init()
        self.touch.Set_Mode(self.mode)
        self.disp.clear()
        self.image = Image.new('RGB', (240, 240), bg_colour)
        self.draw = ImageDraw.Draw(self.image)
        self.Font = ImageFont.truetype(f'lib/{font_name}.ttf', font_size)
        
    def get_input(self):
        if self.mode == 1:
            self.touch.get_point()
            x = self.touch.X_point
            y = self.touch.Y_point
            return x, y
        else:
            return self.touch.Touch_Read_Byte(0x01)
        
    def switch_mode(self, mode):
        self.mode = mode
    
    def update(self):
        self.disp.ShowImage(self.image)
        
    def fill_colour(self, colour='WHITE'):
        self.draw.rectangle((0, 0, 240, 240), fill=colour, outline=None, width=1)
        
    def write(self, text='Hello World!', coordinates=(0, 0), fill='BLACK'):
        self.draw.text(coordinates, text, fill=fill, font=self.Font)
        
    def rectangle(self, coordinates=(0, 0, 240, 240), fill='RED'):
        self.draw.rectangle(coordinates, fill=fill, outline=None, width=1)
        
    def line(self, start=(0, 0), end=(0, 0), width=1, colour='BLACK'):
        self.draw.line((start, end), width=width, fill=colour)
        
    def load_image(self, file_name=None):
        if file_name:
            self.image = Image.open(file_name)
            self.draw = ImageDraw.Draw(self.image)
            
    def main_menu(self):
        self.fill_colour(colour='WHITE')
        self.rectangle(coordinates=(0, 0, 120, 120), fill='crimson')
        self.rectangle(coordinates=(121, 0, 240, 120), fill='cornflowerblue')
        self.rectangle(coordinates=(0, 121, 120, 240), fill='forestgreen')
        self.rectangle(coordinates=(121, 121, 240, 240), fill='gold')
        self.line(start=(120, 0), end=(120, 240), width=4)
        self.line(start=(0, 120), end=(240, 120), width=4)
        self.write(text='Camera', coordinates=(4, 122))
        self.write(text='SMS', coordinates=(128, 122))
        self.write(text='Settings', coordinates=(128, 84))
        self.write(text='Notes', coordinates=(4, 84))
        
    def settings(self, wifi_mode='sim', speaking=True, speaker=True):
        self.fill_colour(colour='red')
        modes = ['wifi', 'sim', 'none']
        wifi_colours = ['green', 'blue', 'gray']
        wifi_colour = wifi_colours[modes.index(wifi_mode)]
        self.rectangle(coordinates=(0, 0, 120, 120), fill=wifi_colour)
        self.rectangle(coordinates=(121, 0, 240, 120), fill='yellow')
        self.rectangle(coordinates=(0, 121, 120, 240), fill='purple')
        self.line(start=(120, 0), end=(120, 240), width=4)
        self.line(start=(0, 120), end=(240, 120), width=4)
        self.write(text='Wifi mode', coordinates=(4, 56))
        self.write(text=wifi_mode, coordinates=(4, 84))
        self.write(text='Speaking', coordinates=(128, 56))
        self.write(text='on' if speaking else 'off', coordinates=(128, 84))
        self.write(text='Speaker', coordinates=(4, 122))
        self.write(text='on' if speaker else 'off', coordinates=(12, 148))
        self.write(text='Exit', coordinates=(128, 122))

    def camera_stream(self, img):
        self.image = img
        self.draw = ImageDraw.Draw(self.iamge)

'''
d = Display()
d.settings()
d.update()'''
