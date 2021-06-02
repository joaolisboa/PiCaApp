import logging


class ImageEffect:

    AVAILABLE_MODES = {'none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint',
                       'hatch', 'gpen', 'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap',
                       'washedout', 'posterise', 'colorpoint', 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2'}

    def __init__(self, camera, value):
        self.camera = camera
        self.value = value

    def run(self):
        if (self.value not in ImageEffect.AVAILABLE_MODES):
            error = 'ImageEffect error: Invalid image_effect'
            logging.error(error)
            return error
        else:
            result = 'ImageEffect: image_effect set to ' + self.value
            logging.info(result)
            self.camera.piCamera.image_effect = self.value
            return result
