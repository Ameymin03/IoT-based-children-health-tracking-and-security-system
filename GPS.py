#!/usr/bin/python
import spidev
import time
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E = 11
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 15
LCD_D7 = 16
# Define sensor channels
count=0
time1=0
&#39;&#39;&#39;

72

define pin for lcd
&#39;&#39;&#39;
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
delay = 1
GPIO.setup(LCD_E, GPIO.OUT) # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7
# Define some device constants
LCD_WIDTH = 16 # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
adc = spi.xfer2([1,(8+channel)&lt;&lt;4,0])
data = ((adc[1]&amp;3) &lt;&lt; 8) + adc[2]
return data
def heartb():
global count
global time1
global count_1
while True:

73

reading = ReadChannel(0)
if reading&gt;0:
lcd_byte(0x01,LCD_CMD) # 000001 Clear display
lcd_string(&quot;PULSE Detected&quot;,LCD_LINE_1)
else:
lcd_byte(0x01,LCD_CMD) # 000001 Clear display
lcd_string(&quot;PULSE not &quot;,LCD_LINE_1)
lcd_string(&quot;detected&quot;,LCD_LINE_2)
count=count+1
time.sleep(0.6)
#print &quot;time1&quot;,time1
time1=time1+0.6
#print &quot;time1:&quot;,time1

if time1&gt;10:
count=10*count
break
count_1=str(count)
count=0
time1=0
lcd_byte(0x01,LCD_CMD) # 000001 Clear display
lcd_string(&quot;Heart Rate =&quot; + count_1,LCD_LINE_1)
return count_1

&#39;&#39;&#39;
Function Name :lcd_init()
Function Description : this function is used to initialized lcd by sending the different
commands
&#39;&#39;&#39;
def lcd_init():

74

# Initialise display
lcd_byte(0x33,LCD_CMD) # 110011 Initialise
lcd_byte(0x32,LCD_CMD) # 110010 Initialise
lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
lcd_byte(0x01,LCD_CMD) # 000001 Clear display
time.sleep(E_DELAY)
&#39;&#39;&#39;
Function Name :lcd_byte(bits ,mode)
Fuction Name :the main purpose of this function to convert the byte data into bit and send to
lcd port
&#39;&#39;&#39;
def lcd_byte(bits, mode):
# Send byte to data pins
# bits = data
# mode = True for character
# False for command
GPIO.output(LCD_RS, mode) # RS
# High bits
GPIO.output(LCD_D4, False)
GPIO.output(LCD_D5, False)
GPIO.output(LCD_D6, False)
GPIO.output(LCD_D7, False)
if bits&amp;0x10==0x10:
GPIO.output(LCD_D4, True)
if bits&amp;0x20==0x20:
GPIO.output(LCD_D5, True)
if bits&amp;0x40==0x40:
GPIO.output(LCD_D6, True)

75

if bits&amp;0x80==0x80:
GPIO.output(LCD_D7, True)
# Toggle &#39;Enable&#39; pin
lcd_toggle_enable()
# Low bits
GPIO.output(LCD_D4, False)
GPIO.output(LCD_D5, False)
GPIO.output(LCD_D6, False)
GPIO.output(LCD_D7, False)
if bits&amp;0x01==0x01:
GPIO.output(LCD_D4, True)
if bits&amp;0x02==0x02:
GPIO.output(LCD_D5, True)
if bits&amp;0x04==0x04:
GPIO.output(LCD_D6, True)
if bits&amp;0x08==0x08:
GPIO.output(LCD_D7, True)
# Toggle &#39;Enable&#39; pin
lcd_toggle_enable()
&#39;&#39;&#39;Function Name : lcd_toggle_enable()
Function Description:basically this is used to toggle Enable pin&#39;&#39;&#39;
def lcd_toggle_enable():
# Toggle enable
time.sleep(E_DELAY)
GPIO.output(LCD_E, True)
time.sleep(E_PULSE)
GPIO.output(LCD_E, False)
time.sleep(E_DELAY)
&#39;&#39;&#39;Function Name :lcd_string(message,line)

76

Function Description :print the data on lcd &#39;&#39;&#39;
def lcd_string(message,line):
# Send string to display
message = message.ljust(LCD_WIDTH,&quot; &quot;)
lcd_byte(line, LCD_CMD)
for i in range(LCD_WIDTH):
lcd_byte(ord(message[i]),LCD_CHR)
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
temp = ((data * 330)/float(1023))
temp = round(temp,places)
return temp
# Define delay between readings
delay = 5
lcd_init()
lcd_string(&quot;welcome &quot;,LCD_LINE_1)
time.sleep(2)
lcd_string(&quot;waiting &quot;,LCD_LINE_1)
lcd_string(&quot; for input &quot;,LCD_LINE_2)
time.sleep(2)
while True:
reading = ReadChannel(0)
if(reading&gt;0):
heartb()
temp_channel = 1
temp_level = ReadChannel(temp_channel)
temp = ConvertTemp(temp_level,0)

77

lcd_string(&quot;Temperature=&quot; +str(temp),LCD_LINE_2)
time.sleep(10)