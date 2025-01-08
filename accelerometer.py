import smbus
import time
import math
 
# ADXL345 I2C Address
ADXL345_I2C_ADDR = 0x53
 
# ADXL345 Registers
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATAX0 = 0x32
DATAX1 = 0x33
DATAY0 = 0x34
DATAY1 = 0x35
DATAZ0 = 0x36
DATAZ1 = 0x37
 
class ADXL345:
    G = 9.81  # Earth's gravity in m/s^2
 
    def __init__(self, bus_num=1):
        self.bus = smbus.SMBus(bus_num)
        # Set range to +/- 16g and FULL_RES bit
        self.bus.write_byte_data(ADXL345_I2C_ADDR, DATA_FORMAT, 0x0B)
        # Turn on the accelerometer
        self.bus.write_byte_data(ADXL345_I2C_ADDR, POWER_CTL, 0x08)
 
    def read_acceleration(self):
        # Read acceleration data
        bytes = self.bus.read_i2c_block_data(ADXL345_I2C_ADDR, DATAX0, 6)
        
        # Convert to 2's complement and then to m/s^2
        x = (bytes[1] << 8 | bytes[0])
        if x & (1 << 15):
            x = x - (1 << 16)
        x = (x / (2**15)) * 16 * self.G
        
        y = (bytes[3] << 8 | bytes[2])
        if y & (1 << 15):
            y = y - (1 << 16)
        y = (y / (2**15)) * 16 * self.G
        
        z = (bytes[5] << 8 | bytes[4])
        if z & (1 << 15):
            z = z - (1 << 16)
        z = (z / (2**15)) * 16 * self.G
        
        return (x, y, z)
 
    def get_tilt_angles(self):
        x, y, z = self.read_acceleration()
        
        pitch = math.degrees(math.atan2(y, math.sqrt(x**2 + z**2)))
        roll = math.degrees(math.atan2(-x, z))
 
        return pitch, roll
 
if __name__ == "__main__":
    accelerometer = ADXL345()
    while True:
        x, y, z = accelerometer.read_acceleration()
        pitch, roll = accelerometer.get_tilt_angles()
        print(f"Acceleration - X: {x:.3f} m/s^2, Y: {y:.3f} m/s^2, Z: {z:.3f} m/s^2")
        print(f"Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")
        time.sleep(0.5)
