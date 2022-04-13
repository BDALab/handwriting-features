import numpy
from handwriting_features.data.utils.math import derivation
from handwriting_features.features.implementation.conventional.spatial import stroke_length
from handwriting_features.features.implementation.conventional.temporal import stroke_duration


class WritingTempoUtils(object):
    """Class implementing writing tempo utils"""

    def __init__(self, sample_wrapper, in_air):
        self.stroke_lengths = stroke_length(sample_wrapper, in_air)
        self.stroke_durations = stroke_duration(sample_wrapper, in_air)

    def get_writing_tempo(self):
        """Extracts the writing tempo"""
        return len(self.stroke_lengths) / (sum(self.stroke_durations) + numpy.finfo(float).eps)


class WritingStopsUtils(object):
    """Class implementing writing stops utils"""

    def __init__(self, sample_wrapper):
        self.strokes = sample_wrapper.strokes
        self.indices = self._get_stroke_indexes([stroke for _, stroke in self.strokes])

    def get_writing_stops(self):
        """Extracts the stroke stops"""

        # Prepare the stops
        time = numpy.nan
        stops_borders_left = []
        stops_borders_right = []

        # Extract the stops
        for (pen_status, stroke), index in zip(self.strokes, self.indices):
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
            border_left, border_right = self._get_borders(velocity)

            # Take only pauses lasting at least 15 ms
            pause_indices = numpy.where((border_right - border_left) > num_samples)[0]
            border_left = border_left[pause_indices].astype(numpy.float)
            border_right = border_right[pause_indices].astype(numpy.float)

            # Fuze the pauses
            border_left, border_right = self._fuze_pauses(border_left, border_right, num_samples)

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

    @classmethod
    def _get_stroke_indexes(cls, strokes):
        """Gets the indexes of the strokes"""

        # Prepare the list of indexes
        indexes = []

        # Get the indexes
        for i in range(len(strokes)):
            if i == 0:
                indexes.append(0)
            else:
                indexes.append(indexes[i - 1] + len(strokes[i - 1].time))

        # Return the indexes
        return indexes

    @classmethod
    def _get_borders(cls, array, border_value=0):
        """Gets borders of an array given a border value"""

        # Get the shifted arrays
        array_l = array[:-1]
        array_r = array[1:]

        # Get the borders
        border_l = numpy.where(numpy.logical_and(array_r == border_value, array_l != border_value))[0]
        border_r = numpy.where(numpy.logical_and(array_r != border_value, array_l == border_value))[0]

        if array[0] == border_value:
            border_l = numpy.array([0] + border_l.tolist())
        if array[-1] == border_value:
            border_r = numpy.array(border_r.tolist() + [len(array)])

        # Return the borders
        return border_l, border_r

    @classmethod
    def _fuze_pauses(cls, border_left, border_right, num_samples):
        """Fuzes the pauses"""

        # Fuze the pauses
        if len(border_left) > 1:
            for i in range(len(border_left) - 1):
                if border_left[i + 1] - border_right[i] < (2 * num_samples):
                    border_left[i + 1], border_right[i] = numpy.nan, numpy.nan

            # Get the improper pauses
            to_remove = [
                i for i, (l, r) in enumerate(zip(border_left, border_right))
                if numpy.isnan(l) and numpy.isnan(r)
            ]

            # Remove improper pauses
            border_left = numpy.delete(border_left, to_remove)
            border_right = numpy.delete(border_right, to_remove)

            # Update the pauses
            nans_right = numpy.isnan(border_right)
            if nans_right.any():

                border_right = numpy.array([
                    border_right[i + 1] if is_nan else border_right[i]
                    for i, is_nan in zip(range(len(border_right)), nans_right)
                ])

                border_left = numpy.delete(border_left, numpy.where(nans_right)[0] + 1)
                border_right = numpy.delete(border_right, numpy.where(nans_right)[0] + 1)

        # Return the fused pauses
        return border_left, border_right


# TODO: in progress
class WritingNumberOfChangesUtils(object):
    """Class implementing writing number of changes utils"""

    # Default computational arguments
    fc = 17.5
    n = 50

    def __init__(self, sample_wrapper):
        pass

    def get_number_of_changes(self, fs, fc=None, n=None):
        """Extracts the number of writing changes

        :param fs: sampling frequency
        :type fs: float
        :param fc: cutoff frequency for the low-pass filter, defaults to 17.5
        :type fc: float, optional
        :param n: number of samples of a Gaussian filter, defaults to 50
        :type n: int
        :return: number of writing changes
        :rtype: numpy.ndarray or numpy.NaN
        """

        # Check the arguments
        fc = fc if fc else self.fc
        n = n if n else self.n

        # Return the number of changes
        return numpy.array([1.0, 2.0] * 6)

    def _filter_with_low_pass_filter(self, signal):
        """Filters an input signal by a low-pass filter"""
        pass

    def _filter_with_gaussian_filter(self, signal):
        """Filters an input signal by a Gaussian filter"""
        pass
