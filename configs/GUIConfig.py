from configs.Config import Config

class GUIConfig(Config):
    config = []

    def __init__(self):
        Config.__init__(self, '/gui_config.json')


guiConfig = GUIConfig()