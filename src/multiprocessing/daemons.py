import multiprocessing as mp
import time as t
import sys

def daemon():
    p = mp.current_process()
    print('Starting :', p.name, p.pid)
    sys.stdout.flush()
    t.sleep(2.0)
    print('Exiting :', p.name, p.pid)
    sys.stdout.flush()
    
def non_daemon():
    p = mp.current_process()
    print('Starting :', p.name, p.pid)
    sys.stdout.flush()
    print('Exiting :', p.name, p.pid)
    sys.stdout.flush()
    
if __name__ == "__main__":
    d = mp.Process(name='daemon', target=daemon)
    d.daemon = True
    
    n = mp.Process(name='non-daemon', target=non_daemon)
    n.daemon = False
    
    d.start()
    t.sleep(1)
    n.start()