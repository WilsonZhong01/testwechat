import threading
import time

# global timer
# global count
# count = 1
def main():
    global timer, count
    print('timer run every 1 min, and this is the %s' %count +' time')
    count += 1
    timer = threading.Timer(1,main)
    timer.start()

if __name__ == '__main__':
    count = 1
    timer = threading.Timer(1,main)
    timer.start()
    time.sleep(3)
    timer.cancel()