import multiprocessing as mp
import time

def worker():
    name = mp.current_process().name
    print(name, 'Starting')
    time.sleep(2.0)
    print(name, 'Exiting')

def my_service():
    name = mp.current_process().name
    print(name, 'Starting')
    time.sleep(3.0)
    print(name, 'Exiting')

if __name__ == "__main__":
    service = mp.Process(name='my_service', target=my_service)
    worker_1 = mp.Process(name='worker 1', target=worker)
    worker_2 = mp.Process(target=worker) #use default name
    
    worker_1.start()
    worker_2.start()
    service.start()
    
    