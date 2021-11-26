import numpy


def derivation(array, order=1):
    """
    Returns a derivation of input <array>.

    :param array: input array
    :type array: numpy.ndarray
    :param order: order of derivation, defaults to 1
    :type order: int, optional
    :return: derivation
    :rtype: numpy.ndarray
    """
    return numpy.diff(array, order, axis=0) if isinstance(array, numpy.ndarray) else numpy.nan
