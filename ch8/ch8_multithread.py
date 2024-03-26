import time
import threading

exit_event = threading.Event()

def task(name,delay):
    while True:
        time.sleep(delay)
        print("%s: %s" % (name, time.time())) #get the current time in seconds since the epoc
        if exit_event.is_set():
            break


#create two new threads
t1 = threading.Thread(target=task, args=("fast-thread", 1))
t2 = threading.Thread(target=task, args=("slow-thread", 5))

#start the threads
t1.start()
t2.start()

#init counter
n=0

#main function
try:
    while True:
        n+=1
        print("Main thread: %s" % n)
        time.sleep(1) 
except KeyboardInterrupt:
    exit_event.set()

