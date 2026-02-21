from machine import Pin
import neopixel
import utime
import math

STRIP_LENGTH = 45
BRIGHTNESS = 1 #adjust for brightness of the LEDs, scale 0-1
ALLIANCE = "red" #change to "blue" for blue alliance

pin_left = Pin(0)
pixel_left = neopixel.NeoPixel(pin_left, STRIP_LENGTH) #strips from last year are 45 lights long

def set_pixel(strip, pixel, color):
    strip[pixel] = (int(color[0] * BRIGHTNESS), int(color[1] * BRIGHTNESS), int(color[2] * BRIGHTNESS))
def fill_strip(strip, color):
    strip.fill((int(color[0] * BRIGHTNESS), int(color[1] * BRIGHTNESS), int(color[2] * BRIGHTNESS)))


def idle():
    global ALLIANCE
    
    tick = int(round(utime.ticks_ms() / 100))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 10
        value = value * 1.5
        value = value ** 2
        value = int(round(value))
        
#         print(value)
        
        if ALLIANCE == "red":
            set_pixel(pixel_left, i, (value, 0, 0))
        elif ALLIANCE == "blue":
            set_pixel(pixel_left, i, (0, 0, value))
        else:
            print("invalid alliance color")

def active():
    global ALLIANCE
    
    tick = int(round(utime.ticks_ms() / 20))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 20
        value = value * 0.8
        value = value ** 2
        value = int(round(value))
        
#         print(value)
                
        if ALLIANCE == "red":
            set_pixel(pixel_left, i, (value, 0, 0))
        elif ALLIANCE == "blue":
            set_pixel(pixel_left, i, (0, 0, value))
        else:
            print("invalid alliance color")

def shoot():
    tick = int(round(utime.ticks_ms() / 35))
    
    for i in range (0, STRIP_LENGTH, 1):
        value = ((i + 50) - tick) % 8
        value = value * 0.9
        value = value ** 3
        value = int(round(value))
        set_pixel(pixel_left, i, (value, int(round(value / 10)), 0))
        
#         print(value)

def target_locked():
    tick = int(round(utime.ticks_ms() / 30))
    
    value = 1 + math.sin(tick / 2)
    value = value * 100
    value = int(round(value))
    
    fill_strip(pixel_left, (0, value, 0))
    
def climbing():
    tick = int(round(utime.ticks_ms() / 10))
    
    cycletick = tick % (STRIP_LENGTH * 5)
    segment_length = STRIP_LENGTH * 1.25
    
    if cycletick < STRIP_LENGTH:
        set_pixel(pixel_left, int(tick % segment_length), (255, 0, 255))
    elif cycletick > STRIP_LENGTH * 1.25 and cycletick < STRIP_LENGTH * 2.25:
        set_pixel(pixel_left, int(tick % segment_length), (0, 0, 0))
    elif cycletick > STRIP_LENGTH * 2.5 and cycletick < STRIP_LENGTH * 3.5:
        set_pixel(pixel_left, int(STRIP_LENGTH - 1 - (tick % segment_length)), (255, 0, 255))
    elif cycletick > STRIP_LENGTH * 3.75 and cycletick < STRIP_LENGTH * 4.75:
        set_pixel(pixel_left, int(STRIP_LENGTH - 1 - (tick % segment_length)), (0, 0, 0))
    elif cycletick == (STRIP_LENGTH * 5) - 1:
        fill_strip(pixel_left, (0, 0, 0))
        # print("clear")

def climbed():
    tick = int(round(utime.ticks_ms() / 30))
    
    value = 1 + math.sin(tick / 8)
    value = value * 100
    value = int(round(value))
    
    fill_strip(pixel_left, (value, 0, value))
          
          
pixel_left.fill((0, 0, 0))
pixel_left.write()

utime.sleep(1)


while True:
    climbed()
    
    utime.sleep_ms(5) #adjust for peak frames per second of the robot, 20ms is approx 50fps max rendering ability
    pixel_left.write()