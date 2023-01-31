import time
import board,busio
import digitalio
from time import sleep
from adafruit_st7735r import ST7735R
import displayio

import neopixel
import adafruit_ds3231

import displayio
import terminalio
from adafruit_display_text import label

from adafruit_bitmap_font import bitmap_font
import rotaryio

import microcontroller

Buzz = digitalio.DigitalInOut(board.GP28)
Buzz.direction = digitalio.Direction.OUTPUT
# Rotary encoder
enc = rotaryio.IncrementalEncoder(board.GP13, board.GP14)
encSw = digitalio.DigitalInOut(board.GP15)
encSw.direction = digitalio.Direction.INPUT
encSw.pull = digitalio.Pull.UP
lastPosition = 0
#-----------------------------------------------------
#
#-----------------------------------------------------
btn_H1 = digitalio.DigitalInOut(board.GP27)
btn_H1.direction = digitalio.Direction.INPUT
btn_H1.pull = digitalio.Pull.DOWN
 
btn_H2 = digitalio.DigitalInOut(board.GP26)
btn_H2.direction = digitalio.Direction.INPUT
btn_H2.pull = digitalio.Pull.DOWN

btn_M1 = digitalio.DigitalInOut(board.GP22)
btn_M1.direction = digitalio.Direction.INPUT
btn_M1.pull = digitalio.Pull.DOWN

btn_M2 = digitalio.DigitalInOut(board.GP19)
btn_M2.direction = digitalio.Direction.INPUT
btn_M2.pull = digitalio.Pull.DOWN

btn_Mode = digitalio.DigitalInOut(board.GP18)
btn_Mode.direction = digitalio.Direction.INPUT
btn_Mode.pull = digitalio.Pull.DOWN

SDA = board.GP20
SCL = board.GP21
i2c = busio.I2C(SCL, SDA)
rtc = adafruit_ds3231.DS3231(i2c)

days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
#----WS2812B
# Update this to match the number of NeoPixel LEDs connected to your board.
fbright=0.05
num_pixels = 17
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = fbright

#-----------------------------------------------------
#      ST7735
#-----------------------------------------------------
mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin_FAKE = board.GP7  #board.GP19
#cs1_pin = board.GP18
cs1 = digitalio.DigitalInOut(board.GP1)
cs1.direction = digitalio.Direction.OUTPUT
cs2 = digitalio.DigitalInOut(board.GP2)
cs2.direction = digitalio.Direction.OUTPUT
cs3 = digitalio.DigitalInOut(board.GP3)
cs3.direction = digitalio.Direction.OUTPUT
cs4 = digitalio.DigitalInOut(board.GP4)
cs4.direction = digitalio.Direction.OUTPUT

dc_pin = board.GP16
cs1.value = False
cs2.value = False
cs3.value = False
cs4.value = False


#--------------------------------------------------------------
displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin_FAKE, reset=reset_pin)
display = ST7735R(display_bus, width=128, height=160, bgr = True)

Nixie_0 = displayio.OnDiskBitmap("/b00.bmp")
Nixie_1 = displayio.OnDiskBitmap("/b01.bmp")
Nixie_2 = displayio.OnDiskBitmap("/b02.bmp")
Nixie_3 = displayio.OnDiskBitmap("/b03.bmp")
Nixie_4 = displayio.OnDiskBitmap("/b04.bmp")
Nixie_5 = displayio.OnDiskBitmap("/b05.bmp")
Nixie_6 = displayio.OnDiskBitmap("/b06.bmp")
Nixie_7 = displayio.OnDiskBitmap("/b07.bmp")
Nixie_8 = displayio.OnDiskBitmap("/b08.bmp")
Nixie_9 = displayio.OnDiskBitmap("/b09.bmp")

GreenB = 0x00CC00
#Enable
cs1.value = True
cs2.value = True
cs3.value = True
cs4.value = True
group = displayio.Group()
display.show(group)
COLOR = (0, 0, 0) 
RR = (250, 0, 0)  # color to blink
GG = (0, 250, 0)
BB = (0, 0, 250) 
pixels.fill((0, 0, 250))
pixels[9] = COLOR
pixels[10] = COLOR
pixels[11] = COLOR
pixels[12] = COLOR
pixels[14] = COLOR
pixels[15] = COLOR
pixels.show()
cntled = 0
TmpH_alarm=""
TmpM_alarm=""
Hourtmp=0
Mintmp=0
tbright=0.0
tbright2="0.05"
fbright=0.06

def Getbright() :
    try:
        file = open("bright.txt", "r")
        tbright2 = file.read()
        print (tbright2)

    except OSError as e:  # Typically when the filesystem isn't writeable...
        print("Err Read alarm")
        with open("/bright.txt", "w") as bright:
            bright.write("0.05")
            bright.flush()
            tbright2="0.05"
            print (tbright2)
            
    tbright=float(tbright2)
    return(tbright)

def GetAlarm() :

    try:
        file = open("alarm.txt", "r")
        content = file.read()
        Talam=content.split(",")
        TmpH_alarm=Talam[1]
        TmpM_alarm=Talam[2]
        print (Talam[0] )
        print (TmpH_alarm)
        print (TmpM_alarm)

    except OSError as e:  # Typically when the filesystem isn't writeable...
        print("Err Read alarm")
        TmpH_alarm='0'
        TmpM_alarm='0'
        
    Hourtmp=int(TmpH_alarm)
    Mintmp=int(TmpM_alarm)
    
    return(Hourtmp, Mintmp)

tmp = GetAlarm()
Hourtmp=tmp[0]
Mintmp=tmp[1]
fbright=Getbright()

if fbright>0.0 :
    #fbright=int(tbright)
    pixels.brightness=fbright
    print("Set Bright OK")

def UpBright ():
    cs3.value = False
    splash2 = displayio.Group()
    display.show(splash2)    
    Hstr= "UP" #f"{Hourtmp:02n}" 
    Hour_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Hstr)
    Hour_label.anchor_point = (1.0, 0.0)
    Hour_label.anchored_position = (97, 45)
    Hour_label.scale = (5)
    splash2.append(Hour_label)
    sleep(.2)
    cs3.value = True
def DnBright ():
    cs3.value = False
    splash2 = displayio.Group()
    display.show(splash2)    
    Hstr= "Down" #f"{Hourtmp:02n}" 
    Hour_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Hstr)
    Hour_label.anchor_point = (1.0, 0.0)
    Hour_label.anchored_position = (127, 45)
    Hour_label.scale = (5)
    splash2.append(Hour_label)
    sleep(.2)
    cs3.value = True
    
def UpYear (Yeartmp2):
    cs4.value = False
    splash2 = displayio.Group()
    display.show(splash2)

    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash2.append(bg_sprite)    
  
    Mstr= f"{Yeartmp2:04n}" 
    Year_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Mstr)
    Year_label.anchor_point = (1.0, 0.0)
    Year_label.anchored_position = (90, 45)
    Year_label.scale = (7)
    splash2.append(Year_label)
    sleep(.2)
    cs4.value = True
    
def UpMon (Montmp):
    cs2.value = False
    splash2 = displayio.Group()
    display.show(splash2)    
    Hstr= f"{Montmp:02n}" 
    Mon_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Hstr)
    Mon_label.anchor_point = (1.0, 0.0)
    Mon_label.anchored_position = (97, 45)
    Mon_label.scale = (7)
    splash2.append(Mon_label)
    sleep(.2)
    cs2.value = True
def UpDay (Daytmp):
    cs4.value = False
    splash2 = displayio.Group()
    display.show(splash2)    
    Mstr= f"{Daytmp:02n}" 
    Day_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Mstr)
    Day_label.anchor_point = (1.0, 0.0)
    Day_label.anchored_position = (97, 45)
    Day_label.scale = (7)
    splash2.append(Day_label)
    sleep(.2)
    cs4.value = True 

def UpHour (Hourtmp):
    cs2.value = False
    splash2 = displayio.Group()
    display.show(splash2)    
    Hstr= f"{Hourtmp:02n}" 
    Hour_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Hstr)
    Hour_label.anchor_point = (1.0, 0.0)
    Hour_label.anchored_position = (97, 45)
    Hour_label.scale = (7)
    splash2.append(Hour_label)
    sleep(.2)
    cs2.value = True
def UpMin (Mintmp):
    cs4.value = False
    splash2 = displayio.Group()
    display.show(splash2)    
    Mstr= f"{Mintmp:02n}" 
    Min_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Mstr)
    Min_label.anchor_point = (1.0, 0.0)
    Min_label.anchored_position = (97, 45)
    Min_label.scale = (7)
    splash2.append(Min_label)
    sleep(.2)
    cs4.value = True
#----------------------------------------------------
#  SET Bright
#----------------------------------------------------
fbright=0.05

def SettingBright(tmpbright):
    fbright2=tmpbright
    SetOK=False
#----------------------------------------------------------
#LCD 1    
    cs1.value = False
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 70, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFF66  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
# Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 66, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x0000CC  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=2)
    splash.append(inner_sprite)

# Draw a label
    text_group = displayio.Group(scale=2, x=11, y=24)
    text = "Brightness \nSETTING"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF66)
    text_group.append(text_area)  # Subgroup for text scaling
    #splash.append(text_group)

    splash.append(text_group)
    #splash.append(Hour2_group)

    sleep(.2)
    splash.remove(text_group)
    splash.remove(inner_sprite)
    splash.remove(bg_sprite)
    cs1.value = True
    sleep(.1)
    
#----------------------------------------------------------
#LCD 2
    cs2.value = False
    splash = displayio.Group()
    display.show(splash)
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Draw a label
    text_group = displayio.Group(scale=3, x=1, y=90)
    text = "Bright>"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    sleep(.2)
    splash.remove(text_group)
    cs2.value = True
    sleep(.1)

#----------------------------------------------------------
#LCD 3
    cs3.value = False
    splash = displayio.Group()
    display.show(splash)
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Draw a label
    text_group = displayio.Group(scale=3, x=1, y=90)
    text = " "
    text_area = label.Label(terminalio.FONT, text=text, color=0x00CCCC)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    sleep(.2)
    splash.remove(text_group)
    cs3.value = True
    sleep(.1)
#----------------------------------------------------------------------------
#LCD 4    
    cs4.value = False
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000 

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    sleep(.2)
    splash.remove(bg_sprite)
    cs4.value = True
    sleep(.1)
#----------------------------------------------------------    
    #UpMin (Mintmp)
    position=0
    lastPosition=0
    #fbright=0.06
#----------------------------------------------------------
    TimeOK = False
    while(TimeOK == False):

        position = enc.position
        if position != lastPosition:
        #led.value = True
            if lastPosition < position:
                print("R")
                if(fbright2<0.55):
                    fbright2=fbright2+0.05
                    pixels.brightness=fbright2
                    UpBright()
                    print(fbright2)
            else:
                print("L")
                if(fbright2>0.05):
                    fbright2=fbright2-0.05
                    pixels.brightness=fbright2
                    DnBright()
                    print(fbright2)
            lastPosition = position
            # poll encoder button
        if encSw.value == 0:
            print("SW")
            try:
                    Hstr= f"{fbright2}"
                    with open("/bright.txt", "w") as bright:
                        bright.write(Hstr)
                        bright.flush()
            except OSError as e:  # Typically when the filesystem isn't writeable...
                        print("Err Write Bright")           
            
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
            TimeOK = True
        if btn_Mode.value:
            print("Exit Bright")
            try:
                    Hstr= f"{fbright2}"
                    with open("/bright.txt", "w") as bright:
                        bright.write(Hstr)
                        bright.flush()
            except OSError as e:  # Typically when the filesystem isn't writeable...
                        print("Err Write Bright") 
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
            TimeOK = True
                
        time.sleep(0.1)
#----------------------------------------------------
#  SET ALARM
#----------------------------------------------------
def SettingAlarm(Year,Mon,Day,Hour,Min):
    try:
        file = open("alarm.txt", "r")
        content = file.read()
        Talam=content.split(",")
        TmpH_alarm=Talam[1]
        TmpM_alarm=Talam[2]
        print (Talam[0] )
        print (TmpH_alarm)
        print (TmpM_alarm)

    except OSError as e:  # Typically when the filesystem isn't writeable...
        print("Err Read alarm")
        TmpH_alarm='0'
        TmpM_alarm='0'
    
    Hourtmp=int(TmpH_alarm)
    Mintmp=int(TmpM_alarm)
    Daytmp=Day
    Montmp=Mon
    Yeartmp=Year
    SetOK=False
#----------------------------------------------------------
#LCD 1    
    cs1.value = False
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 70, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
# Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 66, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0xCC3300  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=2)
    splash.append(inner_sprite)

# Draw a label
    text_group = displayio.Group(scale=2, x=11, y=24)
    text = "ALARM \nSETTING"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    #splash.append(text_group)

    Hour2_group = displayio.Group(scale=3, x=11, y=90)
    Hour2 = "Hour>"
    Hour2_area = label.Label(terminalio.FONT, text=Hour2, color=0x00CCCC)#0xFFFFFF)
    Hour2_group.append(Hour2_area)  # Subgroup for text scaling

    splash.append(text_group)
    splash.append(Hour2_group)

    sleep(.2)
    splash.remove(text_group)
    splash.remove(inner_sprite)
    splash.remove(bg_sprite)
    cs1.value = True
    sleep(.1)
    
#----------------------------------------------------------
#LCD 2

    UpHour (Hourtmp)

    sleep(.1)
#----------------------------------------------------------    
    cs3.value = False
    splash = displayio.Group()
    display.show(splash)
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Draw a label
    text_group = displayio.Group(scale=3, x=1, y=90)
    text = "Minute>"
    text_area = label.Label(terminalio.FONT, text=text, color=0x00CCCC)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    sleep(.2)
    splash.remove(text_group)
    cs3.value = True
    sleep(.1)
#----------------------------------------------------------    
    UpMin (Mintmp)
    
#----------------------------------------------------------
    TimeOK = False
    while(TimeOK == False):

        if btn_H1.value:
            SetOK=True
            print("H1")
            if Hourtmp < 23:
                Hourtmp=Hourtmp+1
            else :
                Hourtmp=0
            UpHour (Hourtmp)
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False

#        if btn_H2.value:
#            print("H2")
#            Buzz.value = True
#            time.sleep(0.1)
#            Buzz.value = False

        if btn_M1.value:
            SetOK=True
            print("M1")
            if Mintmp < 59:
                Mintmp=Mintmp+1
            else :
                Mintmp=0
            UpMin (Mintmp)    
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
        if btn_M2.value:
            SetOK=True
            print("M2")
            if Mintmp < 59:
                Mintmp=Mintmp+1
            else :
                Mintmp=0
            UpMin (Mintmp) 
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False

        if btn_Mode.value:
            print("SetTime")
            if SetOK==True :
                try:
                    Hstr= f"{Hourtmp}"
                    Mstr= f"{Mintmp}"
                    with open("/alarm.txt", "w") as datalog:
                        datalog.write('1')
                        datalog.write(',')
                        datalog.write(Hstr)
                        datalog.write(',')
                        datalog.write(Mstr)
                        datalog.flush()
                        time.sleep(1)
                        TmpH_alarm=Hstr
                        TmpM_alarm=Mstr
                        Hourtmp=int(TmpH_alarm)
                        Mintmp=int(TmpM_alarm)
                except OSError as e:  # Typically when the filesystem isn't writeable...
                        print("Err Write alarm")
 
                try:
                    file = open("alarm.txt", "r")
                    content = file.read()
                    print (content )
            
                except OSError as e:  # Typically when the filesystem isn't writeable...
                    print("Err Read alarm")
         
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
            TimeOK = True
            try:
                #SettingAlarm(Yeartmp,Montmp,Daytmp,TmpH_alarm,TmpM_alarm)
                SettingBright(fbright)
            except Exception:
                print('ERROR Alarm ')
#----------------------------------------------------
# Set YEAR
#----------------------------------------------------
def SettingYear(Year,Mon,Day,Hour,Min):
    Hourtmp=Hour
    Mintmp=Min
    Daytmp=Day
    Montmp=Mon
    #Yeartmp=Year
    if(Year>=2000):
       Yeartmp=Year-2000 
    print(Year)
    SetOK=False
#----------------------------------------------------------
#LCD 1    
    cs1.value = False
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 70, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xCC3333  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
# Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 60, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
    splash.append(inner_sprite)

# Draw a label
    text_group = displayio.Group(scale=2, x=11, y=24)
    text = "YEAR \nSETTING"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    sleep(.2)
    #splash.remove(text_group)
    #splash.remove(inner_sprite)
    #splash.remove(bg_sprite)
    cs1.value = True
    sleep(.1)
    
#----------------------------------------------------------
#LCD 2
#----------------------------------------------------------    
    cs2.value = False
    splash = displayio.Group()
    display.show(splash)
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    Min_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = ">")
    Min_label.anchor_point = (1.0, 0.0)
    Min_label.anchored_position = (97, 45)
    Min_label.scale = (7)
    splash.append(Min_label)
    sleep(.2)
    cs2.value = True

    sleep(.1)
#----------------------------------------------------------    
    cs3.value = False
    splash = displayio.Group()
    display.show(splash)
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    Min_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = "20")
    Min_label.anchor_point = (1.0, 0.0)
    Min_label.anchored_position = (97, 45)
    Min_label.scale = (7)
    splash.append(Min_label)
    sleep(.2)
    cs3.value = True
#----------------------------------------------------------    
    UpYear (Yeartmp)
    
#----------------------------------------------------------
    TimeOK = False
    while(TimeOK == False):
        if btn_H1.value:
            SetOK=True
            print("H1")
            if Yeartmp < 99:
                Yeartmp=Yeartmp+1
            else :
                Yeartmp=1
            UpYear (Yeartmp) 
            Buzz.value = True
            time.sleep(0.03)
            Buzz.value = False

#        if btn_H2.value:
#            print("H2")
#            Buzz.value = True
#            time.sleep(0.1)
#            Buzz.value = False

        if btn_M1.value:
            SetOK=True
            print("M1")
            if Yeartmp < 99:
                Yeartmp=Yeartmp+1
            else :
                Yeartmp=1
            UpYear (Yeartmp)   
            Buzz.value = True
            time.sleep(0.03)
            Buzz.value = False
        if btn_M2.value:
            SetOK=True
            print("M2")
            if Yeartmp < 99:
                Yeartmp=Yeartmp+1
            else :
                Yeartmp=1
            UpYear (Yeartmp)  
            Buzz.value = True
            time.sleep(0.03)
            Buzz.value = False

        if btn_Mode.value:
           
            print("SetYear")
            if SetOK==True :
                
                try:
                    t = time.struct_time((2000+Yeartmp,Montmp, Daytmp , Hourtmp  , Mintmp , 30 , 0   , -1  , -1))
                    print("Setting time to:", t)  # uncomment for debugging
                    rtc.datetime = t
                except Exception:
                    print('ERROR upYear ')

            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
            
            try:
                SettingAlarm(Yeartmp,Montmp,Daytmp,TmpH_alarm,TmpM_alarm)
            except Exception:
                print('ERROR Alarm ')    
                
            TimeOK = True
        #time.sleep(0.1)    
#----------------------------------------------------
#
#----------------------------------------------------
def SettingDate(Year,Mon,Day,Hour,Min):
    Hourtmp=Hour
    Mintmp=Min
    Daytmp=Day
    Montmp=Mon
    Yeartmp=Year
    SetOK=False
#----------------------------------------------------------
#LCD 1    
    cs1.value = False
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 70, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xCC3333  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
# Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 60, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
    splash.append(inner_sprite)

# Draw a label
    text_group = displayio.Group(scale=2, x=11, y=24)
    text = "DATE \nSETTING"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    #splash.append(text_group)

    Hour2_group = displayio.Group(scale=3, x=1, y=90)
    Hour2 = "Mounth>"
    Hour2_area = label.Label(terminalio.FONT, text=Hour2, color=0xFFCC00)#0xFFFFFF)
    Hour2_group.append(Hour2_area)  # Subgroup for text scaling

    splash.append(text_group)
    splash.append(Hour2_group)

    sleep(.2)
    splash.remove(text_group)
    splash.remove(inner_sprite)
    splash.remove(bg_sprite)
    cs1.value = True
    sleep(.1)
    
#----------------------------------------------------------
#LCD 2

    UpMon (Montmp)

    sleep(.1)
#----------------------------------------------------------    
    cs3.value = False
    splash = displayio.Group()
    display.show(splash)
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Draw a label
    text_group = displayio.Group(scale=3, x=1, y=90)
    text = "DAY>"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFCC00)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    sleep(.2)
    splash.remove(text_group)
    cs3.value = True
    sleep(.1)
#----------------------------------------------------------    
    UpDay (Daytmp)
#----------------------------------------------------------
    TimeOK = False
    while(TimeOK == False):
        if btn_H1.value:
            SetOK=True
            print("H1")
            if Montmp < 12:
                Montmp=Montmp+1
            else :
                Montmp=1
            UpMon (Montmp)
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False

#        if btn_H2.value:
#            print("H2")
#            Buzz.value = True
#            time.sleep(0.1)
#            Buzz.value = False

        if btn_M1.value:
            SetOK=True
            print("M1")
            if Daytmp < 31:
                Daytmp=Daytmp+1
            else :
                Daytmp=1
            UpDay (Daytmp)    
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
        if btn_M2.value:
            SetOK=True
            print("M2")
            if Daytmp < 31:
                Daytmp=Daytmp+1
            else :
                Daytmp=1
            UpDay (Daytmp)  
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False

        if btn_Mode.value:
            print("SetTime")
            if SetOK==True :
                t = time.struct_time((Yeartmp,Montmp, Daytmp , Hourtmp  , Mintmp , 30 , 0   , -1  , -1))
                print("Setting time to:", t)  # uncomment for debugging
                rtc.datetime = t
 
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
            try:
                SettingYear(Yeartmp,Montmp,Daytmp,Hourtmp,Mintmp)
            except Exception:
                print('ERROR Year ')
                
            TimeOK = True
   

#----------------------------------------------------
#
#----------------------------------------------------
def SettingTime(Year,Mon,Day,Hour,Min):
    Hourtmp=Hour
    Mintmp=Min
    Daytmp=Day
    Montmp=Mon
    Yeartmp=Year
    SetOK=False
#----------------------------------------------------------
#LCD 1    
    cs1.value = False
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 70, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xCC3333  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
# Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 60, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
    splash.append(inner_sprite)

# Draw a label
    text_group = displayio.Group(scale=2, x=11, y=24)
    text = "TIMER \nSETTING"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    #splash.append(text_group)

    Hour2_group = displayio.Group(scale=3, x=11, y=90)
    Hour2 = "Hour>"
    Hour2_area = label.Label(terminalio.FONT, text=Hour2, color=0xFFCC00)#0xFFFFFF)
    Hour2_group.append(Hour2_area)  # Subgroup for text scaling

    splash.append(text_group)
    splash.append(Hour2_group)

    sleep(.2)
    #splash.remove(text_group)
    #splash.remove(inner_sprite)
    #splash.remove(bg_sprite)
    cs1.value = True
    sleep(.1)
#----------------------------------------------------------
#LCD 2
    UpHour (Hourtmp)
    sleep(.1)
#----------------------------------------------------------    
    cs3.value = False
    splash = displayio.Group()
    display.show(splash)
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
# Draw a label
    text_group = displayio.Group(scale=3, x=1, y=90)
    text = "Minute>"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFCC00)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    sleep(.2)
    splash.remove(text_group)
    cs3.value = True
    sleep(.1)
#----------------------------------------------------------    
    UpMin (Mintmp)
    
#----------------------------------------------------------
    TimeOK = False
    while(TimeOK == False):

        if btn_H1.value:
            SetOK=True
            print("H1")
            if Hourtmp < 23:
                Hourtmp=Hourtmp+1
            else :
                Hourtmp=0
            UpHour (Hourtmp)
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False

#        if btn_H2.value:
#            print("H2")
#            Buzz.value = True
#            time.sleep(0.1)
#            Buzz.value = False

        if btn_M1.value:
            SetOK=True
            print("M1")
            if Mintmp < 59:
                Mintmp=Mintmp+1
            else :
                Mintmp=0
            UpMin (Mintmp)    
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
        if btn_M2.value:
            SetOK=True
            print("M2")
            if Mintmp < 59:
                Mintmp=Mintmp+1
            else :
                Mintmp=0
            UpMin (Mintmp) 
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False

        if btn_Mode.value:
            print("SetTime")
            
            if SetOK==True :
                t = time.struct_time((Yeartmp,Montmp, Daytmp , Hourtmp  , Mintmp , 30 , 0   , -1  , -1))
                print("Setting time to:", t)  # uncomment for debugging
                rtc.datetime = t
 
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
            TimeOK = True
            try:
                SettingDate(Yeartmp,Montmp,Daytmp,Hourtmp,Mintmp)
            except Exception:
                print('ERROR Date ')            
 


def DisplayYearMounth(n):
    cs1.value = False
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 80, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x0000CC  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 70, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
    splash.append(inner_sprite)

# Draw a label
    text_group = displayio.Group(scale=2, x=11, y=24)
    text = "YEAR \nDATE\n\nYakroo108\nDesigned"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    sleep(.2)
    #splash.remove(text_group)
    #splash.remove(inner_sprite)
    #splash.remove(bg_sprite)
    cs1.value = True
    sleep(.1)
    
    cs2.value = False
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Draw a label
    text_group = displayio.Group(scale=3, x=31, y=20)
    text = "YEAR"
    text_area = label.Label(terminalio.FONT, text=text, color=GreenB)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling

#int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
    Hstr= f"{t.tm_year}" 
    Hour_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Hstr)
    Hour_label.anchor_point = (1.0, 0.0)
    Hour_label.anchored_position = (90, 45)
    Hour_label.scale = (7)

    splash.append(text_group)
    splash.append(Hour_label)

    sleep(.2)

    splash.remove(text_group)
    splash.remove(Hour_label)
    splash.remove(bg_sprite)
    cs2.value = True
    sleep(.1)
    
    cs3.value = False
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

# Draw a label
    text_group = displayio.Group(scale=3, x=12, y=20)
    text = "Mounth"
    text_area = label.Label(terminalio.FONT, text=text, color=GreenB)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    Mstr=f"{t.tm_mon:02n}" 
    #Mstr= f"{t.tm_mon}"
    print(Mstr)
    Minute_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Mstr)
    Minute_label.anchor_point = (1.0, 0.0)
    Minute_label.anchored_position = (90, 45)
    Minute_label.scale = (7)

    splash.append(text_group)
    splash.append(Minute_label)
#----------------------------------------------------------
    sleep(.2)

    splash.remove(text_group)
    splash.remove(Minute_label)
    cs3.value = True
    sleep(.1)
    
    cs4.value = False
#Clear screen
    color_bitmap = displayio.Bitmap(128, 160, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Bright Green
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    
# Draw a label
    text_group = displayio.Group(scale=3, x=31, y=20)
    text = "DAY"
    text_area = label.Label(terminalio.FONT, text=text, color=GreenB)#0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling

#int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
    Dstr= f"{t.tm_mday:02n}"
    Day_label = label.Label(terminalio.FONT, color=0xFFFFFF, text = Dstr)
    Day_label.anchor_point = (1.0, 0.0)
    Day_label.anchored_position = (90, 45)
    Day_label.scale = (7)

    splash.append(text_group)
    splash.append(Day_label)    
    
    sleep(.1)
    cs4.value = True
    #splash.remove(text_group)
    #splash.remove(Day_label) 
#----------------------------------------------------------
# Rotary encoder
    #enc = rotaryio.IncrementalEncoder(board.GP13, board.GP14)
    #encSw = digitalio.DigitalInOut(board.GP15)
    #encSw.direction = digitalio.Direction.INPUT
    #encSw.pull = digitalio.Pull.UP
    lastPosition = 0

    TimeOK = False
        # Keep running until the voice is understood by Google
    while(TimeOK == False):

        if btn_Mode.value:
            print("go to Set Time")
            Buzz.value = True
            time.sleep(0.1)
            Buzz.value = False
            TimeOK = True
            splash.remove(text_group)
            splash.remove(inner_sprite)
            splash.remove(bg_sprite)

            try:
                SettingTime(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min)
            except Exception:
                print('ERROR Time ')
            
        time.sleep(0.1)

def WsR(n):
    pixels[0] = RR
    pixels[1] = RR
    pixels[2] = RR
    pixels[3] = RR
    pixels[4] = RR
    pixels[5] = RR    
    pixels[6] = RR
    pixels[7] = RR
    pixels[8] = RR
    pixels[13] = RR
    pixels[16] = RR
    
def WsG(n):
    pixels[0] = GG
    pixels[1] = GG
    pixels[2] = GG
    pixels[3] = GG
    pixels[4] = GG
    pixels[5] = GG    
    pixels[6] = GG
    pixels[7] = GG
    pixels[8] = GG
    pixels[13] = GG
    pixels[16] = GG    

def WsB(n):
    pixels[0] = BB
    pixels[1] = BB
    pixels[2] = BB
    pixels[3] = BB
    pixels[4] = BB
    pixels[5] = BB    
    pixels[6] = BB
    pixels[7] = BB
    pixels[8] = BB
    pixels[13] = BB
    pixels[16] = BB
    
def digit(n):
    if n == 0:
        tile_grid = displayio.TileGrid(Nixie_0, pixel_shader=Nixie_0.pixel_shader)
    if n == 1:
        tile_grid = displayio.TileGrid(Nixie_1, pixel_shader=Nixie_0.pixel_shader)
    if n == 2:
        tile_grid = displayio.TileGrid(Nixie_2, pixel_shader=Nixie_0.pixel_shader)
    if n == 3:
        tile_grid = displayio.TileGrid(Nixie_3, pixel_shader=Nixie_0.pixel_shader)
    if n == 4:
        tile_grid = displayio.TileGrid(Nixie_4, pixel_shader=Nixie_0.pixel_shader)
    if n == 5:
        tile_grid = displayio.TileGrid(Nixie_5, pixel_shader=Nixie_0.pixel_shader)
    if n == 6:
        tile_grid = displayio.TileGrid(Nixie_6, pixel_shader=Nixie_0.pixel_shader)
    if n == 7:
        tile_grid = displayio.TileGrid(Nixie_7, pixel_shader=Nixie_0.pixel_shader)
    if n == 8:
        tile_grid = displayio.TileGrid(Nixie_8, pixel_shader=Nixie_0.pixel_shader)
    if n == 9:
        tile_grid = displayio.TileGrid(Nixie_9, pixel_shader=Nixie_0.pixel_shader)
        
    group.append(tile_grid)
    display.show(group)
    sleep(.2)
    group.remove(tile_grid)
#-------------------------------
#
#-------------------------------
Buzz.value = True
time.sleep(0.2)
Buzz.value = False
time.sleep(0.1)
Buzz.value = True
time.sleep(0.1)
Buzz.value = False
time.sleep(0.1)
Buzz.value = True
time.sleep(0.2)
Buzz.value = False
time.sleep(0.1)


StatAlam=0    
    
while True:
    t = rtc.datetime
    print(
        "The date is {} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
        )
    )
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))

    Hmax = t.tm_hour / 10
    Hmin = t.tm_hour % 10
    MinH = t.tm_min / 10
    MinL = t.tm_min % 10
    
    cs1.value = False
    digit(int(Hmax)) 
    cs1.value = True
    sleep(.1)
    
    cs2.value = False
    digit(int(Hmin)) 
    cs2.value = True
    sleep(.1)
    
    cs3.value = False
    digit(int(MinH))
    cs3.value = True
    sleep(.1)
    
    cs4.value = False
    digit(int(MinL)) 
    cs4.value = True
    sleep(.2)    

    cntled=cntled+1
    if(cntled==1):
        WsR(0)
    if(cntled==2):
        WsG(0)
    if(cntled==3):
        WsB(0)
        cntled=0

    pixels[9] = COLOR
    pixels[10] = COLOR
    pixels[11] = COLOR
    pixels[12] = COLOR
    pixels[14] = COLOR
    pixels[15] = COLOR
    pixels.show()
#----------------------------------------
#
#----------------------------------------
    HNow=int(t.tm_hour)
    MNow=int(t.tm_min)
    print(HNow,"->",Hourtmp)
    print(MNow,"->",Mintmp)

    if(StatAlam==0):
        if((Hourtmp>=0) and (Mintmp!=0)) :
            print("Alarm 0")
        
            if (HNow==Hourtmp):
                if (MNow<=Mintmp):
                    StatAlam=1
                    print("Alarm Active")

    elif(StatAlam==1):
        print("Alarm 1")
        if (MNow>=Mintmp):
            StatAlam=2
            print("Alarm Active")
            
    elif(StatAlam==2):
        print("Alarm 2")
        Buzz.value = True
        time.sleep(0.15)
        Buzz.value = False
        if (MNow>Mintmp):
            StatAlam=0
            print("Stop")
            
    elif(StatAlam==4):
        print("Alarm Button")
        if (MNow>Mintmp):
            StatAlam=0
            print("Stop")          
 #----------------------------------------
    if btn_H1.value:
        StatAlam=4
        print("Stop")
#        if btn_H2.value:
#            print("H2")
#            Buzz.value = True
#            time.sleep(0.1)
#            Buzz.value = False

    if btn_M1.value:
        StatAlam=4
        print("Stop")
    if btn_M2.value:
        StatAlam=4
        print("Stop")            
    if btn_Mode.value:
        Buzz.value = True
        time.sleep(0.2)
        Buzz.value = False
        time.sleep(0.1)
        Buzz.value = True
        time.sleep(0.1)
        Buzz.value = False
        print("Setting Mode")
        DisplayYearMounth(0)
        tmp = GetAlarm()
        Hourtmp=tmp[0]
        Mintmp=tmp[1]
        #Setting(t.tm_hour,t.tm_min)
sleep(.2) 















