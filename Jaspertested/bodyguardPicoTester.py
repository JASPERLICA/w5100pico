try:
    import usocket as socket
except:
    import socket
from machine import Pin,SPI
from sys import exit
import urequests
import network
import time
import _thread


#define a global variable
thread_receiver_alive_flag = False
#server_IP = "192.168.0.102" #server running on my laptop
server_IP = "192.168.11.132" # server running on my computer at banalogic
# Bodyguard Pinout definition
led_panel = Pin(1, Pin.OUT)
upper_camera_trigger = Pin(7, Pin.IN, Pin.PULL_UP)
front_camera_trigger = Pin(8, Pin.IN, Pin.PULL_UP)
rear_camera_trigger = Pin(9, Pin.IN, Pin.PULL_UP)
photoeye_npn = Pin(10, Pin.IN, Pin.PULL_UP)
photoeye_pnp = Pin(5, Pin.IN, Pin.PULL_UP)
led_indicator = Pin(25, Pin.OUT)

portnumber = 10001

# Bodyguard tower DHCP configuration
def w5100_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
#None DHCP
    #nic.ifconfig(('192.168.11.15','255.255.255.0','192.168.11.1','8.8.8.8'))
#DHCP
    nic.ifconfig('dhcp')
      
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
      
def bodyguard_client():
    s = socket.socket()
    s.connect((server_IP, portnumber))#16653
    print("bodyguard tower connected...")
    full_msg = ''
    while True:
            msg1 = s.recv(1024)
            if len(msg1) <= 0:
                break
            full_msg += msg1.decode("utf-8")
            print(full_msg)
            s.send(bytes(f"bodyguard tower received {full_msg} ","utf-8"))
            
def bodyguard_tower_receiver(s,):
    global thread_receiver_alive_flag
    full_msg = ''
    while True:
        try:
            msg = s.recv(128)
            #if msg1.decode('utf-8') == "":
            if msg == "":
                break
            if len(msg) <= 0:
                break
            if msg == "photoyeye is blocking":
                led_panel.value(False) #ON
            if msg == "LED times out":
                led_panel.value(True) #ON
            #full_msg += msg1.decode("utf-8")
            #print(full_msg)
            msg_data = msg.decode("utf-8")
            print(msg_data)
            s.send(bytes(f"bodyguard tower received {msg_data} ","utf-8"))
        except OSError:
            print("Bodyguard server disconnected,recever thread exit")
            thread_receiver_alive_flag = True
            exit()
            
            
#def callback(p):
#   print('pin change', p)

def main():
    
    global thread_receiver_alive_flag
    
    w5100_init()
    
    s = socket.socket()
    s.connect((server_IP, portnumber))#10001
    print("bodyguard tower connected...")
    
    _thread.start_new_thread(bodyguard_tower_receiver,(s,))
    
    #photoeye_npn.irq(trigger=Pin.IRQ_FALLING, handler=callback)
    
    time_update_time = time.time()
    time0 = time.time()
    debounce_time = 0
    toggle =  True
    photoeye_unsend = True
    while True:  
        if photoeye_npn.value() is 0:
            if photoeye_unsend == True:
                s.send(bytes("photoyeye is blocking","utf-8"))
                print("photoyeye is blocking")
                photoeye_unsend = False
                time_update_time = time.time()
        else:
            if photoeye_unsend == False:
                if time.time() - time_update_time >= 2:
                    photoeye_unsend = True
            
            
                
        if upper_camera_trigger.value() == 0:
            s.send(bytes("upper_camera_trigger is tripped","utf-8"))
            print("upper_camera_trigger is tripped")
        if front_camera_trigger.value() == 0:
            s.send(bytes("front_camera_trigger is tripped","utf-8"))
            print("front_camera_trigger is tripped")
        if rear_camera_trigger.value() == 0:
            s.send(bytes("rear_camera_trigger is tripped","utf-8"))
            print("rear_camera_trigger is tripped")
        if thread_receiver_alive_flag == True:
            print("main thread exit....")
            exit()
        if time.time()- time0 >= 1:
            time0 = time.time()
            toggle = not toggle
            led_indicator.value(toggle)
            print("tower is alive...")
      
           
    #bg_receiver_thread.daemon = True
    #bg_receiver_thread.start()
    
    
if __name__ == "__main__":
    main()