from threading import Thread
import time

"""
Thread like object
"""

class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        i = 0
        while True:
           i += 1
           print(f"{self.name} : {i}")
           time.sleep(0.5)

# Test!
sergio = MyThread(name='sergio')
mane = MyThread(name='mane')
kenia = MyThread(name='kenia')
sergio.start(), mane.start(), kenia.start() # single line