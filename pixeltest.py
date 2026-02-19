from machine import Pin
import neopixel
import utime
import math

STRIP_LENGTH = 45

pin_left = Pin(0)
pixel_left = neopixel.NeoPixel(pin_left, STRIP_LENGTH) #strips from last year are 45 lights long


def idle(alliance):
    tick = int(round(utime.ticks_ms() / 100))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 10
        value = value * 1.5
        value = value ** 2
        value = int(round(value))
        
#         print(value)
        
        if alliance == "red":
            pixel_left[i] = (value, 0, 0)
        elif alliance == "blue":
            pixel_left[i] = (0, 0, value)
        else:
            print("invalid alliance color")

def active(alliance):
    tick = int(round(utime.ticks_ms() / 20))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 20
        value = value * 0.8
        value = value ** 2
        value = int(round(value))
        
#         print(value)
                
        if alliance == "red":
            pixel_left[i] = (value, 0, 0)
        elif alliance == "blue":
            pixel_left[i] = (0, 0, value)
        else:
            print("invalid alliance color")

def shoot():
    tick = int(round(utime.ticks_ms() / 35))
    
    for i in range (0, STRIP_LENGTH, 1):
        value = ((i + 50) - tick) % 8
        value = value * 0.9
        value = value ** 3
        value = int(round(value))
        pixel_left[i] = (value, int(round(value / 10)), 0)
        
#         print(value)
        
def target_locked():
    tick = int(round(utime.ticks_ms() / 60))
    value = 1 + math.sin(tick)
    value = value * 100
    value = int(round(value))
    pixel_left.fill((0, value, 0))
            
pixel_left.fill((0, 0, 0))
pixel_left.write()

utime.sleep(1)


while True:
    shoot()
    
    utime.sleep_ms(20)
    pixel_left.write()