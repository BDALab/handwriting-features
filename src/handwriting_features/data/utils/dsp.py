class LowPassFilter(object):
    """Class implementing the low-pass filter"""

    def __init__(self, fs, fc):
        self.fs = fs
        self.fc = fc

    # TODO: in progress
    def filter(self, signal):
        """Filters an input signal by a low-pass filter"""
        return signal


class GaussianFilter(object):
    """Class implementing the Gaussian filter"""

    def __init__(self, fs, n):
        self.fs = fs
        self.n = n

    # TODO: in progress
    def filter(self, signal):
        """Filters an input signal by a Gaussian filter"""
        return signal
