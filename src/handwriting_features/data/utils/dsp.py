import scipy.signal as sc
import numpy as np

class LowPassFilter(object):
    """Class implementing the low-pass filter"""

    def __init__(self, fs, fc):
        self.fs = fs
        self.fc = fc

    def _butter_lowpass_filter(self, data, cutoff, fs, order=10):
        """Private function performing low-pass filtering using Butterworth filter"""
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = sc.butter(order, normal_cutoff, btype='lowpass', analog=False)
        return sc.filtfilt(b, a, data)

    def _bessel_lowpass_filter(self, data, cutoff, fs, order=10):
        """Private function performing low-pass filtering using Bessel filter"""
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = sc.bessel(order, normal_cutoff, btype='lowpass', analog=False)
        return sc.filtfilt(b, a, data)

    def filter(self, signal):
        """Filters an input signal by a low-pass filter"""
        return self._butter_lowpass_filter(signal, self.fc, self.fs)


class GaussianFilter(object):
    """Class implementing the Gaussian filter"""

    def __init__(self, fs, n):
        self.fs = fs
        self.n = n

    def _custom_gaussian_filter(self, data, n_window=50, sigma=10):
        """Filters an input signal by Gaussian window"""
        window = sc.windows.gaussian(n_window, std=sigma)
        window = window / np.sum(window)
        return sc.filtfilt(window, 1, data)

    def filter(self, signal):
        """Filters an input signal by a Gaussian filter"""
        return self._custom_gaussian_filter(signal, self.n)
