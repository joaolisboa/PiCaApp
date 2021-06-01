from actions.Capture import Capture
from actions.Record import Record

class Action:

    def __init__(self, camera, action):
        self.action = action
        self.camera = camera

    def run(self):
        if self.action == 'capture':
            return Capture(self.camera).run()
        elif self.action == 'record':
            return Record(self.camera).run()
