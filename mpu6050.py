from busio import I2C
import board
import digitalio

import time
import adafruit_mpu6050

# Turns on the LED to make sure the pico is alive
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

try:
	i2c = I2C(board.GP15, board.GP14) # First SCL, then SDA
except Exception as e:
	print(f"Something bad happened: {e}")
	
mpu = adafruit_mpu6050.MPU6050(i2c)

while(True):
	print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration))
	print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro))
	print("Temperature: %.2f C"%mpu.temperature)
	print("")
	time.sleep(1)