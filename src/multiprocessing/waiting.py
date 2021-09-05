import multiprocessing as mp
import time
import sys

def daemon():
    print('Starting:', mp.current_process().name)
    time.sleep(2)
    print('Exiting :', mp.current_process().name)

def non_daemon():
    print ('Starting:', mp.current_process().name)
    print ('Exiting :', mp.current_process().name)

if __name__ == "__main__":
    d = mp.Process(name='daemon', target=daemon)
    d.daemon = True
    
    n = mp.Process(name='non-daemon', target=non_daemon)
    n.daemon = False
    
    d.start()
    time.sleep(1.0)
    n.start()
    
    d.join()
    n.join()