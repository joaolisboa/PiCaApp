import threading

class State:

    def __init__(self):
        self._lock = threading.Lock()
        self._running = True

    def stop(self):
        with self._lock:
            self._running = False