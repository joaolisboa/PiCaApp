from Camera import Camera


class Capture:

    def __init__(self, camera: Camera):
        self.camera = camera

    def run(self):
        return self.camera.capture(resolution=(4056, 3040))
