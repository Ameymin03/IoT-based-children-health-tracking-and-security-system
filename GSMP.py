#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import pio
import Ports
#import serial
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pio.uart=Ports.UART () # Define serial port
while(1):
time.sleep(1)
pio.uart.println(&quot;AT&quot;)
time.sleep(1)
pio.uart.println(&quot;AT+CMGF=1&quot;)
time.sleep(1)
pio.uart.println(&quot;AT+CMGS=\&quot;+919922512017\&quot;\r&quot;)
time.sleep(1)
pio.uart.println(&quot;Emergency Button has been pressed by the Children&quot;)
time.sleep(1)
#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import pio
import Ports
GPIO.setmode(GPIO.BOARD)

71

GPIO.setwarnings(False)
pio.uart=Ports.UART () # Define serial port
while 1:
Data=pio.uart.recv()
pio.uart.print(Data)