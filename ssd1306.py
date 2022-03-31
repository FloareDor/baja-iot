from busio import I2C
import board
import digitalio

import time
import adafruit_ssd1306

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

try:
	i2c = I2C(board.GP15, board.GP14) # First SCL, then SDA
except Exception as e:
	print(f"Something bad happened: {e}")
	
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.text('Hello', 0, 0, 0)
oled.text('World', 0, 10, 0)
oled.show()