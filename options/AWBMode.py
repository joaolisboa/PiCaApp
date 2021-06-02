import logging


class AWBMode:

    AVAILABLE_MODES = {'off', 'auto', 'sunlight', 'cloudy', 'shade',
                       'tungsten', 'fluorescent', 'incandescent', 'flash', 'horizon'}

    def __init__(self, camera, value):
        self.camera = camera
        self.value = value

    def run(self):
        if (self.value not in AWBMode.AVAILABLE_MODES):
            error = 'AWB Mode error: Invalid awb_mode'
            logging.error(error)
            return error
        else:
            result = 'AWB Mode: awb_mode set to ' + self.value
            logging.info(result)
            self.camera.piCamera.awb_mode = self.value
            return result
