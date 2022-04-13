import numpy
from handwriting_features.features.implementation.conventional.spatial import stroke_length
from handwriting_features.features.implementation.conventional.temporal import stroke_duration
from handwriting_features.features.implementation.conventional.utils.composite import WritingStopsUtils


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


def writing_stops(sample_wrapper):
    """
    Returns the writing stops.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: writing stops
    :rtype: numpy.ndarray or np.NaN
    """
    return WritingStopsUtils(sample_wrapper).get_writing_stops()


def writing_number_of_changes(sample_wrapper):
    """
    Returns the number of writing changes.

    :param sample_wrapper: sample wrapper object
    :type sample_wrapper: HandwritingSampleWrapper
    :return: number of writing interruptions
    :rtype: numpy.ndarray or np.NaN
    """
    pass
