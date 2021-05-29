from configs.Config import Config

class GUIConfig:
    config = []

    def __init__(self):
        self.config = Config('/gui_config.json')

guiConfig = GUIConfig().config