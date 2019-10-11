# from threading import Thread
# from time import sleep
# from app.controllers.Thread import threaded_function
#
# if __name__ == "__main__":
#     thread = Thread(target = threaded_function, args = (10, ))
#     thread.start()
#     thread.join()
#     print("thread finished...exiting")

import threading
import time

def worker():
    print(threading.currentThread().getName(), 'Starting.')
    time.sleep(2)
    print(threading.currentThread().getName(), 'Exiting')

def my_service():
    print(threading.currentThread().getName(), 'Starting..')
    time.sleep(3)
    print(threading.currentThread().getName(), 'Exiting')

t = threading.Thread(name='my_service', target=my_service)
w = threading.Thread(name='worker', target=worker)
w2 = threading.Thread(target=worker) # use default name

w.start()
w2.start()
t.start()