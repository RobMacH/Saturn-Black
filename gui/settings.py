
from threading import Semaphore

def init():
    
    global recording
    global sem
    sem = Semaphore()
    recording = 0