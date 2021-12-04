import numpy
from handwriting_features.data.utils.math import derivation


def stroke_length(sample_wrapper, in_air):
    """
    Returns stroke length.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: stroke length
    :rtype: numpy.ndarray or np.NaN
    """

    # Get the strokes
    strokes = sample_wrapper.on_surface_strokes \
        if not in_air \
        else sample_wrapper.in_air_strokes

    # Check the presence of strokes
    if not strokes:
        return numpy.nan

    # Get the strokes length
    length = [sum(numpy.sqrt(derivation(stroke.x) ** 2 + derivation(stroke.y) ** 2)) for stroke in strokes]
    length = numpy.array(length)

    # Return the length
    return length


def stroke_height(sample_wrapper, in_air):
    """
    Returns stroke height.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: stroke height
    :rtype: numpy.ndarray or np.NaN
    """

    # Get the strokes
    strokes = sample_wrapper.on_surface_strokes \
        if not in_air \
        else sample_wrapper.in_air_strokes

    # Check the presence of strokes
    if not strokes:
        return numpy.nan

    # Return the stokes height
    return numpy.array([max(stroke.y) - min(stroke.y) for stroke in strokes])


def stroke_width(sample_wrapper, in_air):
    """
    Returns stroke width.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: stroke width
    :rtype: numpy.ndarray or np.NaN
    """

    # Get the strokes
    strokes = sample_wrapper.on_surface_strokes \
        if not in_air \
        else sample_wrapper.in_air_strokes

    # Check the presence of strokes
    if not strokes:
        return numpy.nan

    # Return the stokes width
    return numpy.array([max(stroke.x) - min(stroke.x) for stroke in strokes])
