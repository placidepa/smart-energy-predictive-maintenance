import numpy as np
from collections import deque

class TimeSeriesPreprocessor:
    def __init__(self, window_size=60):
        # Stores the last N readings to form a sequence
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)

    def add_reading(self, voltage, current, power):
        """Appends a new reading and returns a normalized window if full."""
        self.buffer.append([voltage, current, power])
        
        if len(self.buffer) == self.window_size:
            # Convert to numpy array and perform basic Min-Max normalization
            # In production, use standard scaler fitted on training data
            data = np.array(self.buffer)
            normalized_data = (data - np.min(data, axis=0)) / (np.ptp(data, axis=0) + 1e-6)
            return normalized_data
        return None