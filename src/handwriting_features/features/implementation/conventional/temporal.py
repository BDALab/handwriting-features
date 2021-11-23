import numpy


def stroke_duration(sample_wrapper, in_air):
    """
    Returns stroke duration.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: stroke duration
    :rtype: numpy.ndarray or np.NaN
    """

    # Get the strokes
    strokes = sample_wrapper.sample.get_on_surface_strokes() \
        if not in_air \
        else sample_wrapper.sample.get_in_air_strokes()

    # Check the presence of strokes
    if not strokes:
        return numpy.nan

    # Return the stokes duration
    return numpy.array([max(stroke.time) - min(stroke.time) for _, stroke in strokes])


def ratio_of_stroke_durations(sample_wrapper):
    """
    Returns ratio of stroke durations: on-surface / in-air.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: ratio of stroke durations
    :rtype: numpy.ndarray or np.NaN
    """

    # Get on-surface and in-air stroke durations
    on_surface_strokes = stroke_duration(sample_wrapper, in_air=False)
    in_air_strokes = stroke_duration(sample_wrapper, in_air=True)

    # Check the presence of the stroke durations
    if any((not isinstance(on_surface_strokes, numpy.ndarray), not isinstance(in_air_strokes, numpy.ndarray))):
        return numpy.nan

    # Get the ratio between the stroke durations
    ratio = [(x / (y + numpy.finfo(float).eps)) for x, y in zip(on_surface_strokes, in_air_strokes)]
    ratio = numpy.array(ratio) if ratio else numpy.nan

    # Return the ratio
    return ratio


def writing_duration(sample_wrapper, in_air):
    """
    Returns writing duration.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :param in_air: in-air flag
    :type in_air: bool
    :return: writing duration
    :rtype: float
    """
    return numpy.sum(stroke_duration(sample_wrapper, in_air))


def ratio_of_writing_durations(sample_wrapper):
    """
    Returns ratio of writing durations: on-surface / in-air.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: ratio of writing durations
    :rtype: float
    """

    # Get on-surface and in-air writing durations
    on_surface_writing_duration = writing_duration(sample_wrapper, in_air=False)
    in_air_writing_duration = writing_duration(sample_wrapper, in_air=True)

    # Check the presence of the writing durations
    if any((not numpy.isfinite(on_surface_writing_duration), not numpy.isfinite(in_air_writing_duration))):
        return numpy.nan

    # Return the ratio between the writing durations
    return on_surface_writing_duration / (in_air_writing_duration + numpy.finfo(float).eps)
