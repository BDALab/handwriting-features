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
    Returns the writing stops.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: writing stops
    :rtype: numpy.ndarray or np.NaN
    """
    return WritingStopsUtils(sample_wrapper).get_writing_stops()


def writing_number_of_changes(sample_wrapper, fs, fc=None, n=None):
    """
    Returns the number of writing changes.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param fs: sampling frequency
    :type fs: float
    :param fc: cutoff frequency for the low-pass filter, defaults to None
    :type fc: float, optional
    :param n: number of samples of a Gaussian filter, defaults to None
    :type n: int
    :return: number of writing changes
    :rtype: numpy.ndarray or np.NaN
    """
    return WritingNumberOfChangesUtils(sample_wrapper, fs=fs, fc=fc, n=n).get_number_of_changes()
