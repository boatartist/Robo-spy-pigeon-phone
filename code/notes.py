from PIL import Image, ImageDraw
from stt import get_speech
import os
import time
from tflite_test_2 import identify_letter
from datetime import datetime

class Notes:
    path = '/home/pi/Desktop/galah/'
    def __init__(self):
        self.note = []
        self.note_mode = 'menu'
        self.drawing = Image.new('RGB', (192, 192), 'white')
        self.draw = ImageDraw.Draw(self.drawing)
        self.had_new_input = False
        
    def note_menu(self, display, has_new_input, x, y):
        display.notes_menu()
        mode = 'notes'
        in_menu = False
        if has_new_input:
            if x < 120 and y < 120:
                self.note_mode = 'view'
            elif x > 120 and y < 120:
                self.note_mode = 'text'
                self.note = []
            elif x < 120 and y > 120:
                self.note_mode = 'draw'
                self.drawing = Image.new('RGB', (192, 192), 'white')
                self.draw = ImageDraw.Draw(self.drawing)
                self.note = ''
            else:
                mode = None
                in_menu = True
        return display, mode, in_menu
    
    def text_notes(self, display, has_new_input, x, y):
        display.text_notes(self.note)
        if has_new_input:
            if x <= 24:
                self.note = []
                self.note_mode = 'menu'
            elif x >= 216:
                display.write('Transcribing...', (26, 116))
                display.update()
                text = get_speech()
                length = 16
                self.note = [text[0+i:length+i] for i in range(0, len(text), length)]
            elif y >= 216:
                with open(f'{Notes.path}note.txt', 'a') as f:
                    f.write(''.join(self.note))
        return display
    
    def draw_notes(self, display, has_new_input, x, y, prev_x, prev_y):
        display.draw_notes(self.drawing, self.note)
        if has_new_input:
            if 30 <= x <= 210 and 30 <= y <= 210:
                self.draw.rectangle((x-2-24, y-2-24, x+2-24, y+2-24), fill='black', outline=None, width=1)
                if self.had_new_input:
                    self.draw.line(((prev_x-24, prev_y-24), (x-24,y-24)), width=3, fill='black')
            #exit
            elif x <= 24:
                self.note_mode = 'menu'
            #identify or backspace
            elif x >= 216:
                if y < 120:
                    print('identifying letter')
                    self.drawing.save(f'letter.jpg')
                    time.sleep(0.2)
                    self.note += identify_letter(f'letter.jpg')['label'].split(' ')[1]
                    self.drawing = Image.new('RGB', (192, 192), 'white')
                    self.draw = ImageDraw.Draw(self.drawing)
                    print(self.note)
                else:
                    if len(self.note) > 0:
                        self.note = self.note[:-1]
                    else:
                        self.note = ''
            #save
            elif y >= 216:
                with open(f'{Notes.path}note.txt', 'a') as f:
                    f.write(self.note)
                '''files = os.listdir()
                nums = []
                for i in files:
                    if 'drawing' in i:
                        nums.append(int(i[7]))
                nums.sort()
                if len(nums) == 0:
                    num = 0
                elif len(nums) >= 8:
                    num = 0
                else:
                    num = nums[-1] + 1
                display.write(f"Saving as drawing{num}.png", (4, 120))
                display.update()
                pic = Image.new('RGB', (240, 240), 'WHITE')
                draw = ImageDraw.Draw(pic)
                if len(self.drawing[0]):
                    for group in self.drawing:
                        prev = group[0]
                        for pos in group[1:]:
                            draw.line((prev, pos), width=2, fill='black')
                            prev = pos
                pic.save(f'{Notes.path}drawing{num}.png')
                time.sleep(2)'''
                
        self.had_new_input = has_new_input
        return display
    
    def view_notes(self, display, has_new_input):
        files = os.listdir()
        nums = []
        for i in files:
            if 'drawing' in i:
                nums.append(int(i[7]))
        display.show_notes(len(nums))
        if has_new_input:
            self.note_mode = 'menu'
        return display
    
    def update(self, display, has_new_input, x, y, prev_x, prev_y):
        mode = 'notes'
        in_menu = False
        if self.note_mode == 'menu':
            display, mode, in_menu = self.note_menu(display, has_new_input, x, y)
        elif self.note_mode == 'text':
            display = self.text_notes(display, has_new_input, x, y)
        elif self.note_mode == 'draw':
            display = self.draw_notes(display, has_new_input, x, y, prev_x, prev_y)
        elif self.note_mode == 'view':
            display = self.view_notes(display, has_new_input)
        return display, mode, in_menu