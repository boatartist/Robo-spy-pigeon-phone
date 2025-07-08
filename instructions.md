So, what's going to be in the galah?
- Raspberry Pi Zero 2 W
- Waveshare Round 1.28inch Touch LCD
- 3.7V 2000mAh LiPo battery
- Telstra LTE 4GX usb modem
- Raspberry Pi camera
- Raspberry Pi camera cable for Pi Zero
- SD card with Raspbian OS for Pi Zero
- USB microphone
- Adafruit Mini USB 4-Port Hub
- Adafruit PowerBoost 500 Charger board
- ADXL345 Accelerometer
- 3 x 9g micro servos
- Mini HDMI to HDMI adapter
- solderable USB sockets
- custom PCB HAT (TBC)
- small speaker/piezo buzzer
- BC557 transistor (for audio amplification)
- 10uF electrolytic capacitor
- 150 ohm resistor
- 270 ohm resistor
- 33 nF ceramic capacitor
- male and female header pins (lots idk how many)

Also possibly needed:
- hdmi cable
- usb mouse and keyboard
- monitor
- micro-usb power source for charging
- soldering equipment
- optional led or sensor for eye

Next up, software settings:
- Raspbian OS for Pi Zero 2 W
- connect to home wifi
- connect to modem by going to `192.168.0.1`
- raspberry pi configuration enable SPI, I2C, set timezone and locale
- alsamixer confirm microphone connection
- open config.txt with `sudo nano /boot/firmware/config.txt` and add `dtoverlay=audremap,pin=13,func=4` to the bottom, as well as `dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24` where spi is enabled, then save and close
- install all python modules with `sudo apt install python3-xyz`, where xyz is the name of each package, (pip is broken in newer versions of raspbian so we need to do it one at a time)
- install espeak with `sudo apt install -y espeak`
- install vosk (stt) with `pip3 install vosk --break-system-packages` (yes it's a bit sketchy but it didnt' work with python3)
- install picamera `sudo apt-get install python3-picamera2 python3-picamera2` (change this in the code, picamera is outdated we need the new version)
- download all the code and put it on the desktop; command line: `wget https://github.com/boatartist/Robo-spy-pigeon-phone/raw/refs/heads/main/galah.zip`
- check all path names are right by running code on the command line `python3 /home/pi/Desktop/galah/bird.py` (or whatever the file is called)
- run the code and make any changes you need to, there may be compatibility errors
- (change the gpio pin for the speaker power from gpio 24 to gpio 12)
- right click on the audio icon in the top right of the screen, increase the volume, in device profiles turn off hdmi audio and check that av jack is enabled in stereo.
- edit `/home/pi/etc/rc.local` and add the line `sudo python3 /home/pi/Desktop/galah/bird.py &`, which should make your code run on startup but in the background so that if it crashes you can still use the raspberry pi
