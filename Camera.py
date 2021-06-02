from picamera import PiCamera
from datetime import datetime
from Utils import wakeDisplay
from time import sleep
from actions.Action import Action
from options.Option import Option
from configs.CameraConfig import cameraConfig
from configs.GUIConfig import guiConfig
from io import BytesIO
from pydng.core import RPICAM2DNG
import logging

class Camera:

    CAPTURE = 'capture'
    RECORDING = 'recording'
    # add support for the remaining formats - validate which requires additional logic, like in the case of raw
    SUPPORTED_CAPTURE_FORMATS = ('jpeg', 'png')
    DEFAULT_CAPTURE_FORMAT = 'jpeg'

    SUPPORTED_RECORDING_FORMATS = ('h264', 'mjpeg')
    DEFAULT_RECORDING_FORMAT = 'h264'

    def __init__(self):
        self.piCamera = PiCamera()
        self.recording = False
        self.piCamera.resolution = cameraConfig.get('preview_res')
        self.captureResolution = cameraConfig.get('capture_res')
        self.recordingResolution = cameraConfig.get('recording_res')
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
        self.piCamera.start_preview(fullscreen=cameraConfig.fullscreen, window=cameraConfig.getPreviewConfig(config))

        # warn possible gui issue when aspect ratio of preview doesn't match camera resolution
        # todo add warning of preview bigger than display
        # todo move to gui render files
        cameraResRatio = self.piCamera.resolution[0] / self.piCamera.resolution[1]
        previewResRatio = cameraConfig.previewWidth / cameraConfig.previewHeight
        if round(cameraResRatio, 2) != round(previewResRatio, 2):
            logging.warning('GUI warning: preview aspect ratio different than camera resolution')

        # camera warm up
        if warmup:
            sleep(2)

    def stop(self):
        self.piCamera.stop_preview()

    def exit(self):
        self.stop()
        self.piCamera.close()

    def action(self, action):
        return Action(self, action)

    def option(self, option, value):
        return Option(self, option, value)

    def capture(self):
        wakeDisplay()
        # set a delay for taking a picture - helps stabilizing when holding the camera in hand after pressing the display
        sleep(cameraConfig.get('capture_delay'))
        self.piCamera.resolution = self.captureResolution
        filename = self.newFilename(Camera.CAPTURE)

        if filename:
            captureFormat = cameraConfig.get('capture_format', default=Camera.DEFAULT_CAPTURE_FORMAT)

            if captureFormat not in Camera.SUPPORTED_CAPTURE_FORMATS:
                logging.error('CAMERA error: specified capture format is not supported. Defaulting to "jpeg" format')
                captureFormat = Camera.DEFAULT_CAPTURE_FORMAT

            path = cameraConfig.get('save_dir') + filename
            self.piCamera.capture(path + '.' + captureFormat, format=captureFormat)
            
            # if save raw is enabled it'll be saved alongside the standard jpeg
            if cameraConfig.get('save_raw'):
                stream = BytesIO()
                self.piCamera.capture(stream, format='jpeg', bayer=True)
                # restore previous resolution before processing file
                self.piCamera.resolution = cameraConfig.get('preview_res')
                d = RPICAM2DNG()
                output = d.convert(stream)
                with open(path + '.dng', 'wb') as f:
                    f.write(output)
            else:
                # restore previous resolution
                self.piCamera.resolution = cameraConfig.get('preview_res')

            return path

        return ''

    def record(self):
        print('recording: ' + str(self.recording))
        if self.recording:
            self.piCamera.stop_recording()
            self.piCamera.resolution = cameraConfig.get('preview_res')
            return ''
        else:
            wakeDisplay()
            # set a delay for taking a picture - helps stabilizing when holding the camera in hand after pressing the display
            sleep(cameraConfig.get('capture_delay'))
            self.piCamera.resolution = self.recordingResolution
            filename = self.newFilename(Camera.RECORDING)

            if filename:
                recordingFormat = cameraConfig.get('recording_format', default=Camera.DEFAULT_RECORDING_FORMAT)

                if recordingFormat not in Camera.SUPPORTED_RECORDING_FORMATS:
                    logging.error('CAMERA error: specified recording format is not supported. Defaulting to "h264" format')
                    recordingFormat = Camera.DEFAULT_RECORDING_FORMAT

                path = cameraConfig.get('save_dir') + filename
                self.piCamera.start_recording(path + '.' + recordingFormat, format=recordingFormat)
                self.recording = True

                return path

            return ''