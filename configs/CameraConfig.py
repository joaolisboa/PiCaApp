from configs.Config import Config

class CameraConfig(Config):
    config = []

    def __init__(self):
        Config.__init__(self, '/camera_config.json')


cameraConfig = CameraConfig()