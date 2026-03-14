from machine import Pin
import neopixel
import utime
import math

STRIP_LENGTH = 45
BRIGHTNESS = 1 #adjust for brightness of the LEDs, scale 0-1

pin_left = Pin(0)
pixels = neopixel.NeoPixel(pin_left, STRIP_LENGTH) #strips from last year are 45 lights long

dio0 = Pin(18, Pin.IN, Pin.PULL_DOWN)
dio1 = Pin(19, Pin.IN, Pin.PULL_DOWN)
dio2 = Pin(20, Pin.IN, Pin.PULL_DOWN)
dio3 = Pin(21, Pin.IN, Pin.PULL_DOWN)

def set_pixel(strip, pixel, color):
    strip[pixel] = (int(color[0] * BRIGHTNESS), int(color[1] * BRIGHTNESS), int(color[2] * BRIGHTNESS))
def fill_strip(strip, color):
    strip.fill((int(color[0] * BRIGHTNESS), int(color[1] * BRIGHTNESS), int(color[2] * BRIGHTNESS)))
    
def readStatus():
    strstatus = str(dio3.value()) + str(dio2.value()) + str(dio1.value()) + str(dio0.value())
    return int(strstatus, 2)
def setStatus():
    status = readStatus()
    [statusIdleRed, statusIdleBlue, statusActiveRed, statusActiveBlue, statusPassing, statusTargetLocked, statusShoot, statusIntaking, statusPurge][status]()

def statusIdle(alliance):
    tick = int(round(utime.ticks_ms() / 125))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 10
        value = value * 1.5
        value = value ** 2
        value = int(round(value))
        
        if alliance == "red":
            set_pixel(pixels, STRIP_LENGTH - 1 - i, (value, 0, 0))
        elif alliance == "blue":
            set_pixel(pixels, STRIP_LENGTH - 1 - i, (0, 0, value))
        else:
            print("invalid alliance color")
def statusActive(alliance):
    tick = int(round(utime.ticks_ms() / 20))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 20
        value = value * 0.8
        value = value ** 2
        value = int(round(value))

        if alliance == "red":
            set_pixel(pixels, STRIP_LENGTH - 1 - i, (value, 0, 0))
        elif alliance == "blue":
            set_pixel(pixels, STRIP_LENGTH - 1 - i, (0, 0, value))
        else:
            print("invalid alliance color")
            
            
def statusIdleRed():
    statusIdle("red")
def statusIdleBlue():
    statusIdle("blue")
def statusActiveRed():
    statusActive("red")
def statusActiveBlue():
    statusActive("blue")
def statusPassing():
    tick = int(round(0 - utime.ticks_ms() / 100))
    
    for i in range (0, STRIP_LENGTH, 1):
        if (tick + i) % 3 == 0:
            set_pixel(pixels, i, (0, 255, 0))
        else:
            set_pixel(pixels, i, (0, 20, 0))
def statusTargetLocked():
    tick = int(round(utime.ticks_ms() / 20))
    
    value = 1 + math.sin(tick / 2)
    value = value * 100
    value = int(round(value))
    
    fill_strip(pixels, (0, value, 0))
def statusShoot():
    tick = int(round(utime.ticks_ms() / 25))
    
    for i in range (0, STRIP_LENGTH, 1):
        value = ((i + 50) - tick) % 8
        value = value * 0.9
        value = value ** 3
        value = int(round(value))
        set_pixel(pixels, STRIP_LENGTH - 1 - i, (value, int(round(value / 15)), 0))
def statusIntaking():
    tick = int(round(utime.ticks_ms() / 30))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 10
        value = value * 1.5
        value = value ** 2
        value = int(round(value))
        
        set_pixel(pixels, STRIP_LENGTH - 1 - i, (value, int(round(value / 2)), 0)) 
def statusPurge():
    tick = int(round(utime.ticks_ms() / 30))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 10
        value = value * 1.5
        value = value ** 2
        value = int(round(value))
        
        set_pixel(pixels, i, (value, int(round(value / 2)), 0))
        
while True:
    setStatus()
    utime.sleep_ms(5)
    pixels.write()