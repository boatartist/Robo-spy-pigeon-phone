from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import display
import os
from PIL import Image

bg=Image.new('RGB', (240, 240), 'BLACK')
Display = display.Display()
Display.switch_mode(1)
Display.camera_stream(bg)
Display.update()
options = Options()
options.add_argument('window-size=340,340')
driver = webdriver.Chrome(options=options)
driver.set_window_position(500, 500, windowHandle='current')
driver.get('http://google.com')
print('done')
print(driver.get_window_size())
os.system(f'scrot "/home/pi/Desktop/galah/display.jpg"')
img = Image.open("/home/pi/Desktop/galah/display.jpg")
img = img.crop((500, 545, 840, 885))
img = img.resize((170, 170))
bg.paste(img, (35, 35))
print(Display.get_input())
Display.camera_stream(bg)
Display.update()
time.sleep(5)
x, y = Display.get_input()
print(x, y)
actionChains = ActionChains(driver)
actionChains.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), x, y).click().perform()
os.system(f'scrot "/home/pi/Desktop/galah/display.jpg"')
img = Image.open("/home/pi/Desktop/galah/display.jpg")
img = img.crop((500, 545, 840, 885))
img = img.resize((170, 170))
bg.paste(img, (35, 35))
Display.camera_stream(bg)
Display.rectangle((x,y,x+2,y+2))
Display.update()
driver.close()