from __main__ import camera
from actions.Capture import Capture

class Action:

    def __init__(self, action):
        self.action = action

    def run(self):
        if self.action == 'capture':
            return Capture(camera).run()