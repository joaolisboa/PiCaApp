from configs.Config import Config

class CameraConfig:
    config = []

    def __init__(self):
        self.config = Config('/camera_config.json')

cameraConfig = CameraConfig().config