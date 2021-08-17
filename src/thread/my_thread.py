from threading import Thread
import time

class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name= name
    
    def run(self):
        i=0
        while True:
           i=i+1
        #    print(f"{self.name} : {i}")
           time.sleep(0.5)


sergio = MyThread(name='sergio')
mane = MyThread(name='mane')
kenia = MyThread(name='kenia')
sergio.start(), mane.start(), kenia.start()
ide = sergio.get_ident()
print(f" sergio {ide}")