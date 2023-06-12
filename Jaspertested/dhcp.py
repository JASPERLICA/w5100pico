#This code has been tested by Jasper
try:
    import usocket as socket
except:
    import socket
from machine import Pin,SPI
import urequests
import network
import time

def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
#None DHCP
    #nic.ifconfig(('192.168.0.15','255.255.255.0','192.168.0.1','8.8.8.8'))
#DHCP
    nic.ifconfig('dhcp')
    
       
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
        
def main():
    w5x00_init()
    
if __name__ == "__main__":
    main()
