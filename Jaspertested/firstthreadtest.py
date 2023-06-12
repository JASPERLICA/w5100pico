import machine
import utime
import _thread

baton = _thread.allocate_lock()
# We configure the pin of the internal led as an output and
# we assign to internal_led
internal_led = machine.Pin(25, machine.Pin.OUT)
# Function that will block the thread with a while loop
# which will simply display a message every second
def second_thread():
    while True:
        baton.acquire()
        print("Hello, I'm here in the second thread writting every second")
        baton.release()
        utime.sleep(1)
# Function that initializes execution in the second core
# The second argument is a list or dictionary with the arguments
# that will be passed to the function.
def three_thread():
    while True:
        # We acquire the traffic light lock
        baton.acquire()
        print("Hello, I'm here in the second thread writting every second")
        baton.release()
        utime.sleep(1)
        # We release the traffic light lock
        
# Function that initializes execution in the second core
# The second argument is a list or dictionary with the arguments
# that will be passed to the function.
_thread.start_new_thread(second_thread, ())
# Second loop that will block the main thread, and what it will do
# that the internal led blinks every half second
#_thread.start_new_thread(thread_thread, ())
# Second loop that will block the main thread, and what it will do
# that the internal led blinks every half second
while True:
    internal_led.toggle()
    baton.acquire()
    print("Hello, I'm here in the main thread writting every second")
    baton.release()
    utime.sleep(0.25)