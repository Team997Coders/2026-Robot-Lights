from machine import Pin
import neopixel
import utime
import math

STRIP_LENGTH = 45
BRIGHTNESS = 1 #adjust for brightness of the LEDs, scale 0-1
ALLIANCE = "blue" #change to "blue" for blue alliance

STATUS_LIST = ["idle", "active", "shoot", "target_search", "target_locked", "climbing", "climbed", "alert"]

in0 = Pin(2, Pin.IN, Pin.PULL_DOWN)
in1 = Pin(3, Pin.IN, Pin.PULL_DOWN)
in2 = Pin(4, Pin.IN, Pin.PULL_DOWN)

dual_strip_pin = Pin(0)
dual_strip = neopixel.NeoPixel(dual_strip_pin, STRIP_LENGTH) #strips from last year are 45 lights long

def read_status():
    status = in0.value() + (in1.value() * 2) + (in2.value() * 4)
    return status

def set_pixel(strip, pixel, color):
    strip[pixel] = (int(color[0] * BRIGHTNESS), int(color[1] * BRIGHTNESS), int(color[2] * BRIGHTNESS))
def fill_strip(strip, color):
    strip.fill((int(color[0] * BRIGHTNESS), int(color[1] * BRIGHTNESS), int(color[2] * BRIGHTNESS)))


def idle():
    global ALLIANCE
    
    tick = int(round(utime.ticks_ms() / 125))
    
    for i in range (0, STRIP_LENGTH, 1):
        
        value = ((i + 50) - tick) % 10
        value = value * 1.5
        value = value ** 2
        value = int(round(value))
        
#         print(value)
        
        if ALLIANCE == "red":
            set_pixel(dual_strip, i, (value, 0, 0))
        elif ALLIANCE == "blue":
            set_pixel(dual_strip, i, (0, 0, value))
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
            set_pixel(dual_strip, i, (value, 0, 0))
        elif ALLIANCE == "blue":
            set_pixel(dual_strip, i, (0, 0, value))
        else:
            print("invalid alliance color")

def shoot():
    tick = int(round(utime.ticks_ms() / 25))
    
    for i in range (0, STRIP_LENGTH, 1):
        value = ((i + 50) - tick) % 8
        value = value * 0.9
        value = value ** 3
        value = int(round(value))
        set_pixel(dual_strip, i, (value, int(round(value / 10)), 0))
        
#         print(value)

def target_search():
    tick = int(round(0 - utime.ticks_ms() / 100))
    
    for i in range (0, STRIP_LENGTH, 1):
        if (tick + i) % 3 == 0:
            set_pixel(dual_strip, i, (0, 255, 0))
        else:
            set_pixel(dual_strip, i, (0, 20, 0))

def target_locked():
    tick = int(round(utime.ticks_ms() / 20))
    
    value = 1 + math.sin(tick / 2)
    value = value * 100
    value = int(round(value))
    
    fill_strip(dual_strip, (0, value, 0))
    
def climbing():
    tick = int(round(utime.ticks_ms() / 10))
    
    cycletick = tick % (STRIP_LENGTH * 5)
    segment_length = STRIP_LENGTH * 1.25
    
    if cycletick < STRIP_LENGTH:
        set_pixel(dual_strip, int(tick % segment_length), (255, 0, 255))
    elif cycletick > STRIP_LENGTH * 1.25 and cycletick < STRIP_LENGTH * 2.25:
        set_pixel(dual_strip, int(tick % segment_length), (0, 0, 0))
    elif cycletick > STRIP_LENGTH * 2.5 and cycletick < STRIP_LENGTH * 3.5:
        set_pixel(dual_strip, int(STRIP_LENGTH - 1 - (tick % segment_length)), (255, 0, 255))
    elif cycletick > STRIP_LENGTH * 3.75 and cycletick < STRIP_LENGTH * 4.75:
        set_pixel(dual_strip, int(STRIP_LENGTH - 1 - (tick % segment_length)), (0, 0, 0))
    elif cycletick == (STRIP_LENGTH * 5) - 1:
        fill_strip(dual_strip, (0, 0, 0))
        # print("clear")

def climbed():
    tick = int(round(utime.ticks_ms() / 30))
    
    value = 1 + math.sin(tick / 8)
    value = value * 100
    value = value + 50
    value = int(round(value))
    
    fill_strip(dual_strip, (value, 0, value))
    
def alert():
    tick = int(round((0 - utime.ticks_ms() )/ 15))
    
    value = tick % 25
    value = value * 10
    
    fill_strip(dual_strip, (value, value * 0.7, value * 0.6))
          
          
dual_strip.fill((0, 0, 0))
dual_strip.write()

utime.sleep(1)


while True:
    #target_search()
    shoot()
    
    utime.sleep_ms(5) #adjust for peak frames per second of the robot, 20ms is approx 50fps max rendering ability
    dual_strip.write()