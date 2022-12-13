import numpy
from handwriting_features.data.utils.math import derivation
from handwriting_features.features.implementation.conventional.utils.spatial import IntersectionUtils


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


def writing_length(sample_wrapper, in_air):
    """
    Returns writing length.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: writing length
    :rtype: float
    """

    # Get the on-surface/in-air sample data
    sample = sample_wrapper.on_surface_data \
        if not in_air \
        else sample_wrapper.in_air_data

    # Check the presence of sample data
    if not sample:
        return numpy.nan

    # Return the writing length
    return sum(numpy.sqrt(derivation(sample.x) ** 2 + derivation(sample.y) ** 2))


def writing_height(sample_wrapper, in_air):
    """
    Returns writing height.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: writing height
    :rtype: float
    """

    # Get the on-surface/in-air sample data
    sample = sample_wrapper.on_surface_data \
        if not in_air \
        else sample_wrapper.in_air_data

    # Check the presence of sample data
    if not sample:
        return numpy.nan

    # Return the writing height
    return float(numpy.max(sample.y) - numpy.min(sample.y))


def writing_width(sample_wrapper, in_air):
    """
    Returns writing width.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: writing width
    :rtype: float
    """

    # Get the on-surface/in-air sample data
    sample = sample_wrapper.on_surface_data \
        if not in_air \
        else sample_wrapper.in_air_data

    # Check the presence of sample data
    if not sample:
        return numpy.nan

    # Return the writing width
    return float(numpy.max(sample.x) - numpy.min(sample.x))


def number_of_intra_stroke_intersections(sample_wrapper):
    """
    Returns number of intra-stroke intersections.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: number of intra-stroke intersections
    :rtype: numpy.ndarray or np.NaN
    """
    return IntersectionUtils(sample_wrapper).get_number_of_intra_stroke_intersections()


def relative_number_of_intra_stroke_intersections(sample_wrapper):
    """
    Returns relative number of intra-stroke intersections.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: relative number of intra-stroke intersections
    :rtype: numpy.ndarray or np.NaN
    """
    return IntersectionUtils(sample_wrapper).get_relative_number_of_intra_stroke_intersections()


def total_number_of_intra_stroke_intersections(sample_wrapper):
    """
    Returns total number of intra-stroke intersections.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: total number of intra-stroke intersections
    :rtype: int
    """
    return IntersectionUtils(sample_wrapper).get_total_number_of_intra_stroke_intersections()


def relative_total_number_of_intra_stroke_intersections(sample_wrapper):
    """
    Returns relative total number of intra-stroke intersections.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: relative total number of intra-stroke intersections
    :rtype: float
    """
    return IntersectionUtils(sample_wrapper).get_relative_total_number_of_intra_stroke_intersections()


def number_of_inter_stroke_intersections(sample_wrapper):
    """
    Returns number of inter-stroke intersections.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: number of inter-stroke intersections
    :rtype: int
    """
    return IntersectionUtils(sample_wrapper).get_number_of_inter_stroke_intersections()


def relative_number_of_inter_stroke_intersections(sample_wrapper):
    """
    Returns relative number of inter-stroke intersections.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: relative number of inter-stroke intersections
    :rtype: float
    """
    return IntersectionUtils(sample_wrapper).get_relative_number_of_inter_stroke_intersections()
