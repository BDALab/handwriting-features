import numpy
from handwriting_features.features.implementation.conventional.spatial import stroke_length
from handwriting_features.features.implementation.conventional.temporal import stroke_duration


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

    # Get the stroke lengths and durations
    stroke_lengths = stroke_length(sample_wrapper, in_air)
    stroke_durations = stroke_duration(sample_wrapper, in_air)

    # Return the writing tempo
    return len(stroke_lengths) / (sum(stroke_durations) + numpy.finfo(float).eps)
