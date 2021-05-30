from configs.Config import Config

class CameraConfig(Config):
    config = []

    fullscreen = False
    previewWidth = 480
    previewHeight = 320
    x = 0
    y = 0

    def __init__(self):
        Config.__init__(self, '/camera_config.json')

    def previewWindow(self):
        return (self.x, self.y, self.previewWidth, self.previewHeight)

    def getPreviewConfig(self, config):
        if config:
            if 'fullscreen' in config:
                self.fullscreen = config['fullscreen']

            if 'window' in config or self.fullscreen == False:
                self.previewWidth = config['window']['width']
                self.previewHeight = config['window']['height']

                if 'x' in config['window']:
                    self.x = config['window']['x']
                if 'y' in config['window']:
                    self.y = config['window']['y']
        
        return self.previewWindow()


cameraConfig = CameraConfig()