from configs.Config import Config

class GUIConfig(Config):
    config = []

    def __init__(self):
        Config.__init__(self, '/gui_config.json')

    def buttons(self):
        return self.get('buttons')

guiConfig = GUIConfig()