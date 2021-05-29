import os

def wakeDisplay():
    os.system('DISPLAY=:0 xset s reset')