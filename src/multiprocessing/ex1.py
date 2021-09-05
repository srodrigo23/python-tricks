
from multiprocessing import Process
import time

#somee examples are prensted in ths page : 
# https://www.pyimagesearch.com/2019/09/09/multiprocessing-with-opencv-and-python/
# this serie of examples are showed in : https://www.journaldev.com/15631/python-multiprocessing-example

def print_func(continent='Asia'):
    time.sleep(5.0)
    print('The name of continent is : ', continent)

if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa']
    procs = []
    proc = Process(target=print_func)  # instantiating without any argument
    procs.append(proc)
    proc.start()

    # instantiating process with arguments
    for name in names:
        # print(name)
        proc = Process(target=print_func, args=(name,))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()

