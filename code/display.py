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