# Adapting the example in https://learn.adafruit.com/adafruit-oled-featherwing/python-usage
# to use with Raspberry Pi Pico and CircuitPython
import board
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
displayio.release_displays()

i2c = busio.I2C (scl=board.GP5, sda=board.GP4) # This RPi Pico way to call I2C

display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1) # Full screen white
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

#bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
#splash.append(bg_sprite)
 
# Draw a smaller inner rectangle
# inner_bitmap = displayio.Bitmap(118, 54, 1)
# inner_palette = displayio.Palette(1)
# inner_palette[0] = 0x000000  # Black
# inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
# splash.append(inner_sprite)
 
# Draw a label
text = "Speed: 69"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=3, y=10, scale=2)
splash.append(text_area)

text = "Laps: 420"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=3, y=40, scale=2)
splash.append(text_area)

#text = "World"
#text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=32, y=25)
#splash.append(text_area)
 
while True:
    pass
