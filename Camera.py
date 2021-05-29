from picamera import PiCamera
from datetime import datetime
from Utils import wakeDisplay
from time import sleep
from configs.CameraConfig import cameraConfig
from configs.GUIConfig import guiConfig
import logging

class Camera:
    saveDir = '/home/pi/Pictures/HQ/'
    fullscreen = False
    width = 800
    height = 480
    x = 0
    y = 0

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = cameraConfig.get('default_res')
        if cameraConfig.get('show_on_start'):
            self.start(guiConfig.get('preview'))

    def newFilename(self):
        return self.saveDir + 'PIC_'+ datetime.now().strftime("%m%d%Y_%H_%M_%S") + '.jpg'

    def start(self, config, warmup = False):
        wakeDisplay()
        self.loadPreviewConfig(config)
        self.camera.start_preview(fullscreen=self.fullscreen, window=self.previewWindow())

        # warn possible gui issue when aspect ratio of preview doesn't match camera resolution
        # todo add warning of preview bigger than display
        # todo move to gui render files
        cameraResRatio = self.camera.resolution[0] / self.camera.resolution[1]
        previewResRatio = self.width / self.height
        if round(cameraResRatio, 2) != round(previewResRatio, 2):
            logging.warning('GUI warning: preview aspect ratio different than camera resolution')

        # camera warm up
        if warmup:
            sleep(2)

    def stop(self):
        self.camera.stop_preview()

    def previewWindow(self):
        return (self.x, self.y, self.width, self.height)

    def loadPreviewConfig(self, config):
        if config:
            if 'fullscreen' in config:
                self.fullscreen = config['fullscreen']

            if 'window' in config or self.fullscreen == False:
                self.width = config['window']['width']
                self.height = config['window']['height']

                if 'x' in config['window']:
                    self.x = config['window']['x']
                if 'y' in config['window']:
                    self.y = config['window']['y']

    def capture(self, resolution):
        wakeDisplay()
        self.camera.resolution = resolution
        filename = self.newFilename()
        self.camera.capture(filename)
        # reset camera preview to previous state
        return filename