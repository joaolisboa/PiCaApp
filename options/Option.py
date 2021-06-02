from options.ImageEffect import ImageEffect
from options.ExposureMode import ExposureMode
from options.AWBMode import AWBMode


class Option:

    def __init__(self, camera, option, value):
        self.camera = camera
        self.option = option
        self.value = value

    def run(self):
        if self.option == 'awb_mode':
            return AWBMode(self.camera, self.value).run()
        elif self.option == 'exposure_mode':
            return ExposureMode(self.camera, self.value).run()
        elif self.option == 'image_effect':
            return ImageEffect(self.camera, self.value).run()
        else:
            return "Option doesn't exist or not yet supported"
