
import time
from . import config

class LCD_1inch28(config.RaspberryPi):

    width = 240
    height = 240 
    def LCD_WriteReg(self, cmd):
        self.digital_write(self.DC_PIN, self.GPIO.LOW)
        self.spi_writebyte([cmd])
        
    def LCD_WriteData_Byte(self, val):
        self.digital_write(self.DC_PIN, self.GPIO.HIGH)
        self.spi_writebyte([val])
        
    def LCD_Reset(self):
        """Reset the display"""
        self.GPIO.output(self.RST_PIN,self.GPIO.HIGH)
        time.sleep(0.01)
        self.GPIO.output(self.RST_PIN,self.GPIO.LOW)
        time.sleep(0.01)
        self.GPIO.output(self.RST_PIN,self.GPIO.HIGH)
        time.sleep(0.01)
        
    def Init(self):
        """Initialize dispaly"""  
        self.LCD_module_init()   
        self.LCD_Reset()
        
        self.LCD_WriteReg(0xEF)
        self.LCD_WriteReg(0xEB)
        self.LCD_WriteData_Byte(0x14)
        
        self.LCD_WriteReg(0xFE)			 
        self.LCD_WriteReg(0xEF) 

        self.LCD_WriteReg(0xEB)	
        self.LCD_WriteData_Byte(0x14)

        self.LCD_WriteReg(0x84)			
        self.LCD_WriteData_Byte(0x40) 

        self.LCD_WriteReg(0x85)			
        self.LCD_WriteData_Byte(0xFF)

        self.LCD_WriteReg(0x86)			
        self.LCD_WriteData_Byte(0xFF) 

        self.LCD_WriteReg(0x87)		
        self.LCD_WriteData_Byte(0xFF)

        self.LCD_WriteReg(0x88)			
        self.LCD_WriteData_Byte(0x0A)

        self.LCD_WriteReg(0x89)			
        self.LCD_WriteData_Byte(0x21)

        self.LCD_WriteReg(0x8A)		
        self.LCD_WriteData_Byte(0x00)

        self.LCD_WriteReg(0x8B)			
        self.LCD_WriteData_Byte(0x80) 

        self.LCD_WriteReg(0x8C)			
        self.LCD_WriteData_Byte(0x01) 

        self.LCD_WriteReg(0x8D)			
        self.LCD_WriteData_Byte(0x01) 

        self.LCD_WriteReg(0x8E)			
        self.LCD_WriteData_Byte(0xFF) 

        self.LCD_WriteReg(0x8F)			
        self.LCD_WriteData_Byte(0xFF) 


        self.LCD_WriteReg(0xB6)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x20)

        self.LCD_WriteReg(0x36)
        self.LCD_WriteData_Byte(0x08)
    
        self.LCD_WriteReg(0x3A)			
        self.LCD_WriteData_Byte(0x05) 


        self.LCD_WriteReg(0x90)			
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x08) 

        self.LCD_WriteReg(0xBD)			
        self.LCD_WriteData_Byte(0x06)
	
        self.LCD_WriteReg(0xBC)			
        self.LCD_WriteData_Byte(0x00)	

        self.LCD_WriteReg(0xFF)			
        self.LCD_WriteData_Byte(0x60)
        self.LCD_WriteData_Byte(0x01)
        self.LCD_WriteData_Byte(0x04)

        self.LCD_WriteReg(0xC3)			
        self.LCD_WriteData_Byte(0x13)
        self.LCD_WriteReg(0xC4)			
        self.LCD_WriteData_Byte(0x13)

        self.LCD_WriteReg(0xC9)		
        self.LCD_WriteData_Byte(0x22)

        self.LCD_WriteReg(0xBE)			
        self.LCD_WriteData_Byte(0x11)

        self.LCD_WriteReg(0xE1)		
        self.LCD_WriteData_Byte(0x10)
        self.LCD_WriteData_Byte(0x0E)

        self.LCD_WriteReg(0xDF)			
        self.LCD_WriteData_Byte(0x21)
        self.LCD_WriteData_Byte(0x0c)
        self.LCD_WriteData_Byte(0x02)

        self.LCD_WriteReg(0xF0)   
        self.LCD_WriteData_Byte(0x45)
        self.LCD_WriteData_Byte(0x09)
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x26)
        self.LCD_WriteData_Byte(0x2A)

        self.LCD_WriteReg(0xF1)    
        self.LCD_WriteData_Byte(0x43)
        self.LCD_WriteData_Byte(0x70)
        self.LCD_WriteData_Byte(0x72)
        self.LCD_WriteData_Byte(0x36)
        self.LCD_WriteData_Byte(0x37)  
        self.LCD_WriteData_Byte(0x6F)


        self.LCD_WriteReg(0xF2)   
        self.LCD_WriteData_Byte(0x45)
        self.LCD_WriteData_Byte(0x09)
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x26)
        self.LCD_WriteData_Byte(0x2A)

        self.LCD_WriteReg(0xF3)  
        self.LCD_WriteData_Byte(0x43)
        self.LCD_WriteData_Byte(0x70)
        self.LCD_WriteData_Byte(0x72)
        self.LCD_WriteData_Byte(0x36)
        self.LCD_WriteData_Byte(0x37) 
        self.LCD_WriteData_Byte(0x6F)

        self.LCD_WriteReg(0xED)	
        self.LCD_WriteData_Byte(0x1B) 
        self.LCD_WriteData_Byte(0x0B) 

        self.LCD_WriteReg(0xAE)			
        self.LCD_WriteData_Byte(0x77)
	
        self.LCD_WriteReg(0xCD)			
        self.LCD_WriteData_Byte(0x63)		


        self.LCD_WriteReg(0x70)			
        self.LCD_WriteData_Byte(0x07)
        self.LCD_WriteData_Byte(0x07)
        self.LCD_WriteData_Byte(0x04)
        self.LCD_WriteData_Byte(0x0E) 
        self.LCD_WriteData_Byte(0x0F)
        self.LCD_WriteData_Byte(0x09)
        self.LCD_WriteData_Byte(0x07)
        self.LCD_WriteData_Byte(0x08)
        self.LCD_WriteData_Byte(0x03)

        self.LCD_WriteReg(0xE8)			
        self.LCD_WriteData_Byte(0x34)

        self.LCD_WriteReg(0x62)			
        self.LCD_WriteData_Byte(0x18)
        self.LCD_WriteData_Byte(0x0D)
        self.LCD_WriteData_Byte(0x71)
        self.LCD_WriteData_Byte(0xED)
        self.LCD_WriteData_Byte(0x70)
        self.LCD_WriteData_Byte(0x70)
        self.LCD_WriteData_Byte(0x18)
        self.LCD_WriteData_Byte(0x0F)
        self.LCD_WriteData_Byte(0x71)
        self.LCD_WriteData_Byte(0xEF)
        self.LCD_WriteData_Byte(0x70) 
        self.LCD_WriteData_Byte(0x70)

        self.LCD_WriteReg(0x63)			
        self.LCD_WriteData_Byte(0x18)
        self.LCD_WriteData_Byte(0x11)
        self.LCD_WriteData_Byte(0x71)
        self.LCD_WriteData_Byte(0xF1)
        self.LCD_WriteData_Byte(0x70) 
        self.LCD_WriteData_Byte(0x70)
        self.LCD_WriteData_Byte(0x18)
        self.LCD_WriteData_Byte(0x13)
        self.LCD_WriteData_Byte(0x71)
        self.LCD_WriteData_Byte(0xF3)
        self.LCD_WriteData_Byte(0x70) 
        self.LCD_WriteData_Byte(0x70)

        self.LCD_WriteReg(0x64)			
        self.LCD_WriteData_Byte(0x28)
        self.LCD_WriteData_Byte(0x29)
        self.LCD_WriteData_Byte(0xF1)
        self.LCD_WriteData_Byte(0x01)
        self.LCD_WriteData_Byte(0xF1)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x07)

        self.LCD_WriteReg(0x66)			
        self.LCD_WriteData_Byte(0x3C)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0xCD)
        self.LCD_WriteData_Byte(0x67)
        self.LCD_WriteData_Byte(0x45)
        self.LCD_WriteData_Byte(0x45)
        self.LCD_WriteData_Byte(0x10)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x00)

        self.LCD_WriteReg(0x67)			
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x3C)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x01)
        self.LCD_WriteData_Byte(0x54)
        self.LCD_WriteData_Byte(0x10)
        self.LCD_WriteData_Byte(0x32)
        self.LCD_WriteData_Byte(0x98)

        self.LCD_WriteReg(0x74)			
        self.LCD_WriteData_Byte(0x10)	
        self.LCD_WriteData_Byte(0x85)	
        self.LCD_WriteData_Byte(0x80)
        self.LCD_WriteData_Byte(0x00) 
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(0x4E)
        self.LCD_WriteData_Byte(0x00)					
        
        self.LCD_WriteReg(0x98)		
        self.LCD_WriteData_Byte(0x3e)
        self.LCD_WriteData_Byte(0x07)

        self.LCD_WriteReg(0x35)	
        self.LCD_WriteReg(0x21)

        self.LCD_WriteReg(0x11)
        time.sleep(0.12)
        self.LCD_WriteReg(0x29)
        time.sleep(0.02)
  
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        #set the X coordinates
        self.LCD_WriteReg(0x2A)
        self.LCD_WriteData_Byte(0x00)               #Set the horizontal starting point to the high octet
        self.LCD_WriteData_Byte(Xstart)      #Set the horizontal starting point to the low octet
        self.LCD_WriteData_Byte(0x00)               #Set the horizontal end to the high octet
        self.LCD_WriteData_Byte(Xend - 1) #Set the horizontal end to the low octet 
        
        #set the Y coordinates
        self.LCD_WriteReg(0x2B)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(Ystart)
        self.LCD_WriteData_Byte(0x00)
        self.LCD_WriteData_Byte(Yend - 1)

        self.LCD_WriteReg(0x2C) 

    def ShowImage_Windows(self,Xstart,Ystart,Xend,Yend,Image):

        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = self.np.asarray(Image)
        pix = self.np.zeros((self.width,self.height,2), dtype = self.np.uint8)
        pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0),self.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()

        if Xstart > Xend:
            data = Xstart
            Xstart = Xend
            Xend = data
            
        if (Ystart > Yend):        
            data = Ystart
            Ystart = Yend
            Yend = data
            
        if Xstart <= 10:
            Xstart = 10
        if Ystart <= 10:
            Ystart = 10
            
        Xstart -= 10;Xend += 10
        Ystart -= 10;Yend += 10
        
        self.SetWindows ( Xstart, Ystart, Xend, Yend)
        self.digital_write(self.DC_PIN,self.GPIO.HIGH)
        for i in range (Ystart,Yend-1):             
            Addr = (Xstart * 2) + (i * 240 * 2)                
            self.spi_writebyte(pix[Addr : Addr+((Xend-Xstart)*2)])


    def ShowImage(self,Image):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = self.np.asarray(Image)
        pix = self.np.zeros((self.width,self.height,2), dtype = self.np.uint8)
        pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0),self.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN,self.GPIO.HIGH)
        for i in range(0,len(pix),4096):
            self.spi_writebyte(pix[i:i+4096])		
    
    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN,self.GPIO.HIGH)
        for i in range(0,len(_buffer),4096):
            self.spi_writebyte(_buffer[i:i+4096])	        
        

