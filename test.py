from busio import I2C
import board
import digitalio

from time import sleep

# Turns on the LED to make sure the pico is alive
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# Rapid blinking: Not all devices connected
def notAllDevicesConnected():
	print("ERROR: Not all devives are connected! Check and try again!")
	while(True):
		led.value = not led.value
		sleep(0.1)

# Fast blinking: I2C not working
def i2cNotWorking():
	while(True):
		led.value = not led.value
		sleep(0.25)

# Mediumish blinking: Pull up resistor
def i2cNoPullUp():
	print("ERROR: No pull up resistor found")
	while(True):
		led.value = not led.value
		sleep(0.5)

try:
	i2c = I2C(board.GP15, board.GP14) # First SCL, then SDA
	i2c2 = I2C(board.GP1, board.GP0)
except RuntimeError:
	i2cNoPullUp()
except Exception as e:
	print(f"Something bad happened: {e}")
	i2cNotWorking()

if(not i2c.try_lock()):
	i2cNotWorking()

while(True):
	print(i2c.scan())
	
	sleep(1)