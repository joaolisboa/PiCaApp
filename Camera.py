from picamera import PiCamera
from datetime import datetime
from Utils import wakeDisplay
from time import sleep
from configs.CameraConfig import cameraConfig
from configs.GUIConfig import guiConfig

class Camera:
    saveDir = '/home/pi/Pictures/HQ/'
    fullscreen = False
    width = 480
    height = 320
    x = 0
    y = 0

    def __init__(self):
        self.camera = PiCamera()
        print(cameraConfig.get('show_on_start'))
        print(guiConfig.get('preview'))
        if cameraConfig.get('show_on_start'):
            self.start(guiConfig.get('preview'))

    def newFilename(self):
        return self.saveDir + 'PIC_'+ datetime.now().strftime("%m%d%Y_%H_%M_%S") + '.jpg'

    def start(self, config, warmup = False):
        wakeDisplay()
        self.loadPreviewConfig(config)
        self.camera.start_preview(fullscreen=self.fullscreen, window=self.previewWindow())
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
        print(self.camera.resolution)
        self.camera.resolution = resolution
        filename = self.newFilename()
        self.camera.capture(filename)
        print(self.camera.resolution)
        # reset camera preview to previous state
        return filename