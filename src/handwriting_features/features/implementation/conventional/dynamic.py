def azimuth(sample_wrapper, in_air):
    """
    Returns azimuth.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: azimuth
    :rtype: numpy.ndarray or np.NaN
    """
    return sample_wrapper.compute_azimuth(in_air)


def tilt(sample_wrapper, in_air):
    """
    Returns tilt.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: tilt
    :rtype: numpy.ndarray or np.NaN
    """
    return sample_wrapper.compute_tilt(in_air)


def pressure(sample_wrapper):
    """
    Returns pressure.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: pressure
    :rtype: numpy.ndarray or np.NaN
    """
    return sample_wrapper.compute_pressure()
