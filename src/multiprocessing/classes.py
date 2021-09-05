import multiprocessing
import time

# Direction to this page og this examples
# https://pymotw.com/2/multiprocessing/basics.html

# Flush
# https://www.geeksforgeeks.org/python-sys-stdout-flush/

class Worker(multiprocessing.Process):

    def run(self):
        time.sleep(6)
        print (f'In {self.name} {self.pid}')


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = Worker()
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()