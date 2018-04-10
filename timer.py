import threading
import time

count = 1
def fun_timer():

    print('timer run every 1 min, and this is the %s' %count +' time')
    count = + 1
    global timer
    timer = threading.Timer(1,fun_timer)

    timer.start()


# timer = threading.Timer(1,fun_timer)
# timer.start()

time.sleep(15)
timer.cancel()