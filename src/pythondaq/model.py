import time
import numpy as np


class Experiment:
    def scan(self, start, stop, steps):
        """Perform a scan over a range with specified steps and return the scanned values."""
        x = np.linspace(start, stop, steps)
        y = []
        for u in x:
            y.append(np.sin(u))
            time.sleep(0.1)
        return x, y
