from tkinter import *
from tkinter import ttk
from configs.CameraConfig import cameraConfig
from configs.GUIConfig import guiConfig
from Camera import Camera
import os
import sys
import logging

class Window:

    def __init__(self, camera: Camera):
        self.camera = camera
        if os.environ.get('DISPLAY','') == '':
            print('No display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        self.root = Tk()
        self.windowWidth = self.root.winfo_screenwidth()
        self.windowHeight = self.root.winfo_screenheight()
        

    def render(self):
        self.root.title(__name__)
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # keep tracking of buttons placement to avoid overlapping
        heightIndex = 0
        widthIndex = cameraConfig.previewWidth

        # render buttons from gui config
        for button in guiConfig.buttons():
            label = button['label']
            buttonHeight = button['height']
            buttonWidth = (self.windowWidth-cameraConfig.previewWidth) if button['width'] == 'auto' else button['width']

            if (widthIndex + buttonWidth) > self.windowWidth:
                logging.warning('GUI warning: buttons outside of frame') 

            action = self.camera.action('capture')
            btn = ttk.Button(self.root, text=label, command=lambda: action.run())
            btn.place(x=widthIndex, y=heightIndex, height = buttonHeight, width = buttonWidth)

            heightIndex += buttonHeight
            widthIndex += buttonWidth
            if (widthIndex + buttonWidth) > self.windowWidth:
                # move to next line
                widthIndex = cameraConfig.previewWidth

        def close():
            sys.exit()

        btn = ttk.Button(self.root, text='Close', command= close)
        btn.place(x=widthIndex, y=heightIndex, height = buttonHeight, width = buttonWidth)

        self.root.mainloop()