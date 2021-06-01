
class Record:

    def __init__(self, camera):
        self.camera = camera

    def run(self):
        return self.camera.record()

