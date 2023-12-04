import time
import numpy as np
import threading


class Experiment:
    def __init__(self):
        self.x = []
        self.y = []

    def start_scan(self, start, stop, steps):
        """Start a new thread to execute a scan."""
        self._scan_thread = threading.Thread(
            target=self.scan, args=(start, stop, steps)
        )
        self._scan_thread.start()

    def scan(self, start, stop, steps):
        """Perform a scan over a range with specified steps and return the scanned values."""
        x = np.linspace(start, stop, steps)
        self.x = []
        self.y = []
        for u in x:
            self.x.append(u)
            self.y.append(np.sin(u))
            time.sleep(0.03)
        return self.x, self.y
