import numpy
from handwriting_features.data.utils.math import derivation
from handwriting_features.features.implementation.conventional.utils import (
    get_stroke_indexes,
    get_borders,
    fuze_pauses
)


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
    strokes = sample_wrapper.on_surface_strokes \
        if not in_air \
        else sample_wrapper.in_air_strokes

    # Check the presence of strokes
    if not strokes:
        return numpy.nan

    # Return the stokes duration
    return numpy.array([max(stroke.time) - min(stroke.time) for stroke in strokes])


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


def writing_duration_overall(sample_wrapper):
    """
    Returns overall writing duration.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: overall writing duration
    :rtype: float
    """
    return float(sample_wrapper.sample_time[-1] - sample_wrapper.sample_time[0])


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


def number_of_interruptions(sample_wrapper):
    """
    Returns the number of interruptions.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: number of interruptions
    :rtype: float
    """

    # Get the pen status
    pen_status = sample_wrapper.sample_pen_status

    # Return the number of interruptions
    return float(max(sum(abs(numpy.logical_xor(pen_status[:-1], pen_status[1:]))), 0))


def number_of_interruptions_relative(sample_wrapper):
    """
    Returns the number of interruptions relative to the duration.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: number of interruptions relative to the duration
    :rtype: float
    """

    # Get the number of interruptions and the overal writing duration
    interruptions = number_of_interruptions(sample_wrapper)
    duration = writing_duration_overall(sample_wrapper)

    # Return the number of interruptions relative to the duration
    return interruptions / (duration + numpy.finfo(float).eps)


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

    # Import the sub-features (import here to avoid circular imports)
    from handwriting_features.features.implementation.conventional.spatial import stroke_length

    # Get the stroke lengths and durations
    stroke_lengths = stroke_length(sample_wrapper, in_air)
    stroke_durations = stroke_duration(sample_wrapper, in_air)

    # Return the writing tempo
    return len(stroke_lengths) / (sum(stroke_durations) + numpy.finfo(float).eps)


def writing_stops(sample_wrapper):
    """
    Returns the writing stops.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: writing stops
    :rtype: numpy.ndarray or np.NaN
    """

    # Get the strokes and their starting indices
    strokes = sample_wrapper.strokes
    indices = get_stroke_indexes([stroke for _, stroke in strokes])

    # Prepare the stops
    time = numpy.nan
    stops_borders_left = []
    stops_borders_right = []

    # Extract the stops
    for (pen_status, stroke), index in zip(strokes, indices):
        if pen_status == "in_air":
            continue

        # Compute the vector of length, time
        length = numpy.sqrt(numpy.power(derivation(stroke.x), 2) + numpy.power(derivation(stroke.y), 2))
        time = derivation(stroke.time)

        # Compute the vector of velocity (value <= 1 mm/s is set to 0)
        velocity = (d / t for (d, t) in zip(length, time))
        velocity = numpy.array([0 if v <= 1 else v for v in velocity])

        # Get the number of samples equaling to 15 ms
        num_samples = numpy.ceil(0.015 / numpy.mean(time))

        # Identify the stops
        border_left, border_right = get_borders(velocity)

        # Take only pauses lasting at least 15 ms
        pause_indices = numpy.where((border_right - border_left) > num_samples)[0]
        border_left = border_left[pause_indices].astype(numpy.float)
        border_right = border_right[pause_indices].astype(numpy.float)

        # Fuze the pauses
        border_left, border_right = fuze_pauses(border_left, border_right, num_samples)

        # Add the starting index of the stroke
        border_left += index
        border_right += index - 1

        # Append the borders to the stops
        stops_borders_left += border_left.tolist()
        stops_borders_right += border_right.tolist()

    # Get the writing stops
    stops = (numpy.array(stops_borders_right) - numpy.array(stops_borders_left)) * numpy.mean(time)
    stops = numpy.array(stops)

    # Return the writing stops
    return stops
