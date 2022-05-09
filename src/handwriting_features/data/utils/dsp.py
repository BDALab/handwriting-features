import scipy.signal as sc
import numpy as np


class LowPassFilter(object):
    """Class implementing the low-pass filter"""

    def __init__(self, fs, fc):
        self.fs = fs
        self.fc = fc

    @staticmethod
    def _get_wn(cutoff, fs):
        """Private method returning the normalized cutoff frequency"""
        return cutoff / (0.5 * fs)

    @classmethod
    def _butter_lowpass_filter(cls, data, cutoff, fs, order=10):
        """Private method performing low-pass filtering using Butterworth filter"""

        # Prepare the coefficients
        coefficients = sc.butter(order, cls._get_wn(cutoff, fs), btype="lowpass", analog=False, output="ba")

        # Filter the input signal
        return sc.filtfilt(*coefficients, data)

    @classmethod
    def _bessel_lowpass_filter(cls, data, cutoff, fs, order=10):
        """Private method performing low-pass filtering using Bessel filter"""

        # Prepare the coefficients
        coefficients = sc.bessel(order, cls._get_wn(cutoff, fs), btype="lowpass", analog=False, output="ba")

        # Filter the input signal
        return sc.filtfilt(*coefficients, data)

    def filter(self, signal):
        """Filters an input signal by a low-pass filter"""
        return self._butter_lowpass_filter(signal, self.fc, self.fs)


class GaussianFilter(object):
    """Class implementing the Gaussian filter"""

    def __init__(self, fs, n):
        self.fs = fs
        self.n = n

    @classmethod
    def _custom_gaussian_filter(cls, data, n_window=50, sigma=10):
        """Private function performing Gaussian filtration"""

        # Prepare the Gaussian window
        window = sc.windows.gaussian(n_window, std=sigma)
        window = window / np.sum(window)

        # Filter the input signal
        return sc.filtfilt(window, 1, data)

    def filter(self, signal):
        """Filters an input signal by a Gaussian filter"""
        return self._custom_gaussian_filter(signal, self.n)
