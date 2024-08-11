import time
from . import config

class Touch_1inch28(config.RaspberryPi):

    def init(self):
        self.Touch_module_init()   
        self.Touch_Reset()

        bRet = self.WhoAmI()
        if bRet:
            print("Success:Detected CST816T.")
            Rev = self.Read_Revision()
            print("CST816T Revision = %d."%Rev)
            self.Stop_Sleep()
        else:
            print("Error: Not Detected CST816T.\r\n")
            return false

    def Touch_Write_Byte(self, cmd, val):
        self.i2c_write_byte(cmd, val)

    def Touch_Read_Byte(self, cmd):
        return self.i2c_read_byte(cmd)

    def WhoAmI(self):
        if (0xB5) != self.Touch_Read_Byte(0xA7):
            return False
        return True

    def Read_Revision(self):
        return self.Touch_Read_Byte(0xA9)

    #Stop sleeping  停止睡眠
    def Stop_Sleep(self):
        self.Touch_Write_Byte(0xFE,0x01)
    
    #Reset  复位    
    def Touch_Reset(self):
        self.GPIO.output(self.TP_RST,self.GPIO.LOW)
        time.sleep(0.01)
        self.GPIO.output(self.TP_RST,self.GPIO.HIGH)
        time.sleep(0.05) 

    #Set mode  设置模式   
    def Set_Mode(self,mode,callback_time=10,rest_time=5): 
        # mode = 0 gestures mode 
        # mode = 1 point mode 
        # mode = 2 mixed mode 
        if (mode == 1):      
            self.Touch_Write_Byte(0xFA,0X41)
            
        elif (mode == 2) :
            self.Touch_Write_Byte(0xFA,0X71)
            
        else:
            self.Touch_Write_Byte(0xFA,0X11)
            self.Touch_Write_Byte(0xEC,0X01)
     
    #Get the coordinates of the touch  获取触摸的坐标
    def get_point(self):
        xy_point = [0,0,0,0]

        xy_point[0] = self.Touch_Read_Byte(0x03)
        xy_point[1] = self.Touch_Read_Byte(0x04)
        xy_point[2] = self.Touch_Read_Byte(0x05)
        xy_point[3] = self.Touch_Read_Byte(0x06)
        
        x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
        y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
        
        self.X_point=x_point
        self.Y_point=y_point


