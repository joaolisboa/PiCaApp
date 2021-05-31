from picamera import PiCamera
from datetime import datetime
from Utils import wakeDisplay
from time import sleep
from actions.Action import Action
from configs.CameraConfig import cameraConfig
from configs.GUIConfig import guiConfig
from io import BytesIO
from pydng.core import RPICAM2DNG
import logging

class Camera:

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = cameraConfig.get('default_res')
        if cameraConfig.get('show_on_start'):
            self.start(guiConfig.get('preview'))

    def newFilename(self):
        return cameraConfig.get('save_dir') + 'PIC_'+ datetime.now().strftime("%m%d%Y_%H_%M_%S")

    def start(self, config, warmup = False):
        wakeDisplay()
        self.camera.start_preview(fullscreen=cameraConfig.fullscreen, window=cameraConfig.getPreviewConfig(config))

        # warn possible gui issue when aspect ratio of preview doesn't match camera resolution
        # todo add warning of preview bigger than display
        # todo move to gui render files
        cameraResRatio = self.camera.resolution[0] / self.camera.resolution[1]
        previewResRatio = cameraConfig.previewWidth / cameraConfig.previewHeight
        if round(cameraResRatio, 2) != round(previewResRatio, 2):
            logging.warning('GUI warning: preview aspect ratio different than camera resolution')

        # camera warm up
        if warmup:
            sleep(2)

    def stop(self):
        self.camera.stop_preview()

    def exit(self):
        self.stop()
        self.camera.close()

    def action(self, action):
        return Action(self, action)

    def capture(self, resolution):
        wakeDisplay()
        # set a delay for taking a picture - helps stabilizing when holding the camera in hand after pressing the display
        sleep(cameraConfig.get('capture_delay'))
        previousResolution = self.camera.resolution
        self.camera.resolution = resolution
        filename = self.newFilename()

        self.camera.capture(filename + '.jpg')
        # if save raw is enabled it'll be saved alongside the standard jpeg
        if cameraConfig.get('save_raw'):
            stream = BytesIO()
            self.camera.capture(stream, format='jpeg', bayer=True)
            # restore previous resolution before processing file
            self.camera.resolution = previousResolution
            d = RPICAM2DNG()
            output = d.convert(stream)
            with open(filename + '.dng', 'wb') as f:
                f.write(output)
        else:
            # restore previous resolution
            self.camera.resolution = previousResolution

        return filename