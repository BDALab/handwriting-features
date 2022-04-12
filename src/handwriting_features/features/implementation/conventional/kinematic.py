import numpy


def velocity(sample_wrapper, axis, in_air):
    """
    Returns velocity.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param axis: axis to compute the velocity from
    :type axis: str
    :param in_air: in-air flag
    :type in_air: bool
    :return: velocity
    :rtype: numpy.ndarray or np.NaN
    """
    return sample_wrapper.compute_velocity(axis, in_air)


def acceleration(sample_wrapper, axis, in_air):
    """
    Returns acceleration.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param axis: axis to compute the acceleration from
    :type axis: str
    :param in_air: in-air flag
    :type in_air: bool
    :return: acceleration
    :rtype: numpy.ndarray or np.NaN
    """
    return sample_wrapper.compute_acceleration(axis, in_air)


def jerk(sample_wrapper, axis, in_air):
    """
    Returns jerk.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param axis: axis to compute the jerk from
    :type axis: str
    :param in_air: in-air flag
    :type in_air: bool
    :return: jerk
    :rtype: numpy.ndarray or np.NaN
    """
    return sample_wrapper.compute_jerk(axis, in_air)
