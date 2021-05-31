from actions.Capture import Capture

class Action:

    def __init__(self, camera, action):
        self.action = action
        self.camera = camera

    def run(self):
        if self.action == 'capture':
            return Capture(self.camera).run()