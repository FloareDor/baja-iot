from busio import I2C
import board
import digitalio

from time import sleep

# Turns on the LED to make sure the pico is alive
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# Rapid blinking: I2C not working
def i2cNotWorking():
	while(True):
		led.value = not led.value
		sleep(0.1)

try:
	i2c = I2C(board.GP15, board.GP14) # First SCL, then SDA
except Exception as e:
	print(f"Something bad happened: {e}")
	i2cNotWorking()

if(not i2c.try_lock()):
	i2cNotWorking()

while(True):
	data0 = bytearray(256)
	data1 = bytearray(256)
	
	i2c.readfrom_into(0x30, data0)
	i2c.readfrom_into(0x30, data1)

	print(list(data0))
	print(list(data1))
	sleep(1)