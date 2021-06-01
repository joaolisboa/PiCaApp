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

    CAPTURE = 'capture'
    RECORDING = 'recording'
    # add support for the remaining formats - validate which requires additional logic, like in the case of raw
    SUPPORTED_FORMATS = ('jpeg', 'png')
    DEFAULT_FORMAT = 'jpeg'

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = cameraConfig.get('preview_res')
        self.photoResolution = cameraConfig.get('camera_res')
        if cameraConfig.get('show_on_start'):
            self.start(guiConfig.get('preview'))

    def newFilename(self, type):
        filename = str()
        filenameFormat = cameraConfig.get('filename_format')

        if type == Camera.CAPTURE: 
            if 'prepend_photo' in filenameFormat:
                filename += filenameFormat['prepend_photo']
        elif type == Camera.RECORDING:
            if 'prepend_video' in filenameFormat:
                filename += filenameFormat['prepend_video']

        # todo - figure out if we should allow this to be mandatory or not to ensure unique filenames or automatically add an alternative
        if 'date_format' in filenameFormat:
            filename += datetime.now().strftime(filenameFormat['date_format'])
        else:
            logging.warning('FILE warning: adding a date format is recommended to guarantee unique filenames')

        # todo - does append make sense??
        if 'append' in filenameFormat:
            filename += filenameFormat['append']

        if not filename:
            logging.error('FILE error: a filename format must be specified')

        return filename

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

    def capture(self):
        wakeDisplay()
        # set a delay for taking a picture - helps stabilizing when holding the camera in hand after pressing the display
        sleep(cameraConfig.get('capture_delay'))
        previousResolution = self.camera.resolution
        self.camera.resolution = self.photoResolution
        filename = self.newFilename(Camera.CAPTURE)

        if filename:
            captureFormat = cameraConfig.get('capture_format', default=Camera.DEFAULT_FORMAT)

            if captureFormat not in Camera.SUPPORTED_FORMATS:
                logging.error('CAMERA error: specified capture format is not supported. Defaulting to "jpeg" format')
                captureFormat = Camera.DEFAULT_FORMAT

            path = cameraConfig.get('save_dir') + filename
            self.camera.capture(path + '.' + captureFormat, format=captureFormat)
            
            # if save raw is enabled it'll be saved alongside the standard jpeg
            if cameraConfig.get('save_raw'):
                stream = BytesIO()
                self.camera.capture(stream, format='jpeg', bayer=True)
                # restore previous resolution before processing file
                self.camera.resolution = previousResolution
                d = RPICAM2DNG()
                output = d.convert(stream)
                with open(path + '.dng', 'wb') as f:
                    f.write(output)
            else:
                # restore previous resolution
                self.camera.resolution = previousResolution

            return path

        return ''