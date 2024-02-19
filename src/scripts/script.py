# To make a deamon in macos
# https://stackoverflow.com/questions/9522324/running-python-in-background-on-os-x
"""
doc string
"""
import urllib.request

def connect(host='http://google.com'):
    """
    Esta es una prueba de documentacion
    """
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

# test

print("connected" if connect() else "no internet!")
