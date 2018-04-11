import threading
import time

# count = 0
def main():
    global count, timer
    count += 1
    print('timer runs every 1 min, and this is the %s' %count +' time')

    # rebuild timer
    timer = threading.Timer(1,main)
    timer.start()

def timer_fun():
    timer = threading.Timer(1, main)
    timer.start()


if __name__ == '__main__':
    # run fun every 1 min
    count = 0
    timer_fun()
    time.sleep(5 * 1)
    timer.cancel()

