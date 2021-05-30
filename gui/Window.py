from tkinter import *
from tkinter import ttk
import os

class Window:

    def __init__(self):
        if os.environ.get('DISPLAY','') == '':
            print('No display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        self.root = Tk()
        

    def render(self):
        self.root.title(__name__)
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        mainframe = ttk.Frame(self.root)
        self.root.mainloop()