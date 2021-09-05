import sys
import time

for i in range(10):
    print(i, end=' ', flush = True)
    # sys.stdout.flush()
    time.sleep(1)
    