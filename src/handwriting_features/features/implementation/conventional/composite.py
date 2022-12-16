from handwriting_features.features.implementation.conventional.utils.composite import (
    WritingTempoUtils,
    WritingStopsUtils,
    WritingNumberOfChangesUtils
)


def writing_tempo(sample_wrapper, in_air):
    """
    Returns writing tempo.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: writing tempo
    :rtype: float
    """
    WritingTempoUtils(sample_wrapper, in_air).get_writing_tempo()


def writing_stops(sample_wrapper):
    """
    Returns writing stops.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: writing stops
    :rtype: numpy.ndarray or np.NaN
    """
    return WritingStopsUtils(sample_wrapper).get_writing_stops()


def number_of_changes_in_x_profile(sample_wrapper, fs, fc=None, n=None):
    """
    Returns number of changes in x profile.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: number of changes in x profile
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_number_of_changes_in_x_profile()


def number_of_changes_in_y_profile(sample_wrapper, fs, fc=None, n=None):
    """
    Returns number of changes in y profile.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: number of changes in y profile
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_number_of_changes_in_y_profile()


def number_of_changes_in_azimuth(sample_wrapper, fs, fc=None, n=None):
    """
    Returns number of changes in azimuth.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: number of changes in azimuth
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_number_of_changes_in_azimuth()


def number_of_changes_in_tilt(sample_wrapper, fs, fc=None, n=None):
    """
    Returns number of changes in tilt.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: number of changes in tilt
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_number_of_changes_in_tilt()


def number_of_changes_in_pressure(sample_wrapper, fs, fc=None, n=None):
    """
    Returns number of changes in pressure.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: number of changes in pressure
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_number_of_changes_in_pressure()


def number_of_changes_in_velocity_profile(sample_wrapper, fs, fc=None, n=None):
    """
    Returns number of changes in velocity profile.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: number of changes in velocity profile
    :rtype: int
    """
    return WritingNumberOfChangesUtils(
        sample_wrapper=sample_wrapper,
        fs=fs,
        fc=fc,
        n=n).get_number_of_changes_in_velocity_profile()


def relative_number_of_changes_in_x_profile(sample_wrapper, fs, fc=None, n=None):
    """
    Returns relative number of changes in x profile.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: relative number of changes in x profile
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_relative_number_of_changes_in_x_profile()


def relative_number_of_changes_in_y_profile(sample_wrapper, fs, fc=None, n=None):
    """
    Returns relative number of changes in y profile.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: relative number of changes in y profile
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_relative_number_of_changes_in_y_profile()


def relative_number_of_changes_in_azimuth(sample_wrapper, fs, fc=None, n=None):
    """
    Returns relative number of changes in azimuth.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: relative number of changes in azimuth
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_relative_number_of_changes_in_azimuth()


def relative_number_of_changes_in_tilt(sample_wrapper, fs, fc=None, n=None):
    """
    Returns relative number of changes in tilt.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: relative number of changes in tilt
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_relative_number_of_changes_in_tilt()


def relative_number_of_changes_in_pressure(sample_wrapper, fs, fc=None, n=None):
    """
    Returns relative number of changes in pressure.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: relative number of changes in pressure
    :rtype: int
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_relative_number_of_changes_in_pressure()


def relative_number_of_changes_in_velocity_profile(sample_wrapper, fs, fc=None, n=None):
    """
    Returns relative number of changes in velocity profile.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int, optional
    :return: relative number of changes in velocity profile
    :rtype: int
    """
    return WritingNumberOfChangesUtils(
        sample_wrapper=sample_wrapper,
        fs=fs,
        fc=fc,
        n=n).get_relative_number_of_changes_in_velocity_profile()
