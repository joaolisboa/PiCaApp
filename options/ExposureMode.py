import logging


class ExposureMode:

    AVAILABLE_MODES = {'off', 'auto', 'night', 'nightpreview', 'backlight', 'spotlight',
                       'sports', 'snow', 'beach', 'verylong', 'fixedfps', 'antishake', 'fireworks'}

    def __init__(self, camera, value):
        self.camera = camera
        self.value = value

    def run(self):
        if (self.value not in ExposureMode.AVAILABLE_MODES):
            error = 'ExposureMode error: Invalid exposure_mode'
            logging.error(error)
            return error
        else:
            result = 'ExposureMode: exposure_mode set to ' + self.value
            logging.info(result)
            self.camera.piCamera.exposure_mode = self.value
            return result
