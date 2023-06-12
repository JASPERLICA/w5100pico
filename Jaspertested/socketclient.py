try:
    import usocket as socket
except:
    import socket
from machine import Pin,SPI
import urequests
import network
import time
portnumber = 12348
#W5x00 chip init
def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
#None DHCP
    nic.ifconfig(('192.168.0.15','255.255.255.0','192.168.0.1','8.8.8.8'))
#DHCP
    #nic.ifconfig('dhcp')
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
def socketclient():
    s = socket.socket()
    s.connect(("192.168.0.102", portnumber))#16653
    print("let it start")
    full_msg = ''
    while True:
            msg1 = s.recv(1024)
            if len(msg1) <= 0:
                break
            full_msg += msg1.decode("utf-8")
            print(full_msg)
            s.send(bytes(f"{full_msg}","utf-8"))
def main():
    w5x00_init()
    socketclient()
if __name__ == "__main__":
    main()