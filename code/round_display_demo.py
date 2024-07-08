#libraries you have to import
import time
import spidev as SPI
from PIL import Image, ImageDraw, ImageFont

#you need to download the demo and unzip it, and in it is a folder called 'lib', put this wherever your code is, so that you can just access the fancy files with this line
from lib import LCD_1inch28, Touch_1inch28

#follow the wiring instructions on the wiki which will organise the pins as follows: (I don't actually know if you need these lines, but they were on the demo and I haven't tried deleting them yet)
RST = 27
DC = 25
BL = 18
TP_INT = 4 #this one does seem to be important

#there are 2 modes, 0 for gestures and 1 for coordinates (I think)
Mode = 0

#create the touch object
touch = Touch_1inch28.Touch_1inch28()

#I haven't quite figured out this function, I think it's part of the way the touch object is set up and how you get gesture/coordinate info, but I don't know if you can bypass it or not
def Int_Callback(TP_INT):
  if Mode == 1:
    touch.get_point()
  else:
    touch.Gestures = touch.Touch_Read_Byte(0x01)

#this is the main loop/section, all within a try-except statement because we don't trust our coding abilities and errors are scary
try:
  #create the display object
  disp = LCD_1inch28.LCD_1inch28()
  #initialise the objects
  disp.Init()
  touch.init()
  #something scary, idrk what this does, but as I said above I think it's part of how input is got, check it out urself ig
  touch.int_irq(TP_INT, Int_Callback)
  
  disp.clear() #we don't want whatever manky code you ran last time now do we?, this probs isn't necessary but it seems like good practice
  
  image = Image.new('RGB', (disp.width, disp.height), 'WHITE') #lots of info here, this is an Image object from the fantastic PIL library, setup with the display object's coordinates (pretend it's a square we just can't see the corners), rgb settings and a white background
  #this is so we can draw on the image, because ✨graphic design is my passion✨
  draw = ImageDraw.Draw(image)
  
  Mode = 0 # I know we already did this, but what if we forgot? better safe than sorry
  touch.Set_Mode(Mode) #we're in gesture mode now
  
  #24 was the smaller font size used in the example, the other one was 35, if that's useful
  Font = ImageFont.truetype('lib/Font00.ttf', 24) #this will cause an error if you run it unless you've put a font file from the demo into the 'lib' folder we copied over, or use another font
  
  #a while loop waiting for you to complete a gesture, your options are:
  #UP: 0x01
  #Down: 0x02
  #left: 0x03
  #right: 0x04
  #double click: 0x0B
  #long press: 0x0C
  
  #let's use double click for this example
  while touch.Gestures != 0x0B:
    draw.rectangle((0, 0, 240, 240), fill='WHITE', outline=None, width=1) #fill the entire display with a white rectangle
    draw.text((0, 0), 'Hello World!', fill='BLACK', font=Font) #puts 'Hello World!' in the top left corner, this is a bad position, it will be cut off, but that's ok
    disp.ShowImage(image) #make sure to actually show the image!
    time.sleep(0.001) #wait to see if they do anything, otherwise this will run too fast
  
  #now for the coordinates mode
  Mode = 1
  touch.Set_Mode(Mode)
  
  #setup the colour we're drawing with
  colour = 'RED'
  #reset the image by filling it all with white
  draw.rectangle((0, 0, 240, 240), fill='WHITE', outline=None, width=1)
  disp.ShowImage(image)
  
  #I'm going to loop for 100 seconds or 100,000 miliseconds, but this might as well be an infinite loop
  for _ in range(100000):
    #if there is touch input, ie finger is on screen
    if touch.X_point != 0:
      x = touch.X_point
      y = touch.Y_point
      draw.rectangle((x, y, x+2, y+2), fill=colour, outline=None, width=1) #draw a pixel wherever the user presses
    disp.ShowImage(image)
    time.sleep(0.001) #sleep for 1 milisecond

except: #if we get errors
  print('Oops, errors')
  #do something else maybe
