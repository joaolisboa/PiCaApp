from Camera import Camera
import threading

class State:

    def __init__(self, camera: Camera):
        self._lock = threading.Lock()
        self._running = True
        self.camera = camera

    def stop(self):
        with self._lock:
            self._running = False