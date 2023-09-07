import numpy
import functools
from copy import deepcopy
from handwriting_features.data.utils.math import derivation
from handwriting_features.data.utils.dsp import LowPassFilter, GaussianFilter
from handwriting_features.data.exceptions.dsp import FiltrationError
from handwriting_features.features.implementation.conventional.spatial import stroke_length
from handwriting_features.features.implementation.conventional.temporal import stroke_duration


class WritingTempoUtils(object):
    """Class implementing writing tempo utils"""

    def __init__(self, sample_wrapper, in_air):
        """Initializes the writing tempo utils object"""

        # Set the stroke lengths and durations
        self.stroke_lengths = stroke_length(sample_wrapper, in_air)
        self.stroke_durations = stroke_duration(sample_wrapper, in_air)

    def get_writing_tempo(self):
        """Extracts the writing tempo"""
        return len(self.stroke_lengths) / (sum(self.stroke_durations) + numpy.finfo(float).eps)


class WritingStopsUtils(object):
    """Class implementing writing stops utils"""

    def __init__(self, sample_wrapper):
        """Initializes the writing stops utils object"""

        # Set the strokes and indices
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
            border_left = border_left[pause_indices].astype(float)
            border_right = border_right[pause_indices].astype(float)

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


class WritingNumberOfChangesUtils(object):
    """Class implementing writing number of changes utils"""

    # Default computational arguments
    fc = 17.5
    n = 50

    def __init__(self, sample_wrapper, fs, fc=None, n=None, subset=None):
        """
        Initializes the writing number of changes utils object.

        :param fs: sampling frequency
        :type fs: float
        :param fc: cutoff frequency for the low-pass filter, defaults to 17.5
        :type fc: float, optional
        :param n: number of samples of a Gaussian filter, defaults to 50
        :type n: int, optional
        :param subset: subset of composite features to return, defaults to None
        :type subset: list, optional
        """

        # Set the sample wrapper
        self.sample_wrapper = deepcopy(sample_wrapper)

        # Set the DSP arguments
        self.fs = fs
        self.fc = fc if fc else WritingNumberOfChangesUtils.fc
        self.n = n if n else WritingNumberOfChangesUtils.n

        # Set the filter instances
        self.low_pass_filter = LowPassFilter(self.fs, self.fc)
        self.gaussian_filter = GaussianFilter(self.fs, self.n)

        # Get the duration
        self.duration = self.sample_wrapper.sample_time[-1] - self.sample_wrapper.sample_time[0]

        # Filter x, y, azimuth, tilt, and pressure by a low-pass filter
        self.sample_wrapper.sample = self._filter_data_with_low_pass_filter(self.sample_wrapper.sample)

        # Get the on-surface strokes
        self.strokes = self.sample_wrapper.on_surface_strokes

        # Set the subset of the features to return
        self.subset = subset

    @functools.lru_cache(maxsize=1)
    def get_number_of_changes_in_x_profile(self):
        """Gets the number of changes in x profile"""
        return sum(self._get_changes(self._filter_data_with_gaussian_filter(s).x) for s in self.strokes)

    @functools.lru_cache(maxsize=1)
    def get_number_of_changes_in_y_profile(self):
        """Gets the number of changes in y profile"""
        return sum(self._get_changes(self._filter_data_with_gaussian_filter(s).y) for s in self.strokes)

    @functools.lru_cache(maxsize=1)
    def get_number_of_changes_in_azimuth(self):
        """Gets the number of changes in azimuth"""
        return sum(self._get_changes(self._filter_data_with_gaussian_filter(s).azimuth) for s in self.strokes)

    @functools.lru_cache(maxsize=1)
    def get_number_of_changes_in_tilt(self):
        """Gets the number of changes in tilt"""
        return sum(self._get_changes(self._filter_data_with_gaussian_filter(s).tilt) for s in self.strokes)

    @functools.lru_cache(maxsize=1)
    def get_number_of_changes_in_pressure(self):
        """Gets the number of changes in pressure"""
        return sum(self._get_changes(self._filter_data_with_gaussian_filter(s).pressure) for s in self.strokes)

    @functools.lru_cache(maxsize=1)
    def get_number_of_changes_in_velocity_profile(self):
        """Gets the number of changes in velocity profile"""

        # Prepare the number of changes
        num_changes = 0

        # Compute the number of changes
        for stroke in self.strokes:

            # Compute the vector of length, time, and velocity
            length = numpy.sqrt(numpy.power(derivation(stroke.x), 2) + numpy.power(derivation(stroke.y), 2))
            time = derivation(stroke.time)
            velocity = numpy.array([d / t for (d, t) in zip(length, time)])

            # Filter the velocity by a Gaussian filter
            try:
                velocity = self._filter_velocity_with_gaussian_filter(velocity)
            except FiltrationError:
                print(f"Filtration error: skipping stroke {stroke}")
                continue

            # Compute the number of changes
            num_changes += self._get_changes(velocity)

        # Return the number of changes
        return num_changes

    def get_relative_number_of_changes_in_x_profile(self):
        """Gets the relative number of changes in x profile"""
        return self.get_number_of_changes_in_x_profile() / self.duration

    def get_relative_number_of_changes_in_y_profile(self):
        """Gets the relative number of changes in y profile"""
        return self.get_number_of_changes_in_y_profile() / self.duration

    def get_relative_number_of_changes_in_azimuth(self):
        """Gets the relative number of changes in azimuth"""
        return self.get_number_of_changes_in_azimuth() / self.duration

    def get_relative_number_of_changes_in_tilt(self):
        """Gets the relative number of changes in tilt"""
        return self.get_number_of_changes_in_tilt() / self.duration

    def get_relative_number_of_changes_in_pressure(self):
        """Gets the relative number of changes in pressure"""
        return self.get_number_of_changes_in_pressure() / self.duration

    def get_relative_number_of_changes_in_velocity_profile(self):
        """Gets the relative number of changes in velocity profile"""
        return self.get_number_of_changes_in_velocity_profile() / self.duration

    @classmethod
    def _get_changes(cls, signal):
        """Gets the changes"""

        # Get the left/right side changes
        changes_left = numpy.sum(numpy.logical_and(signal[1:-1] > signal[:-2], signal[1:-1] > signal[2:]))
        changes_right = numpy.sum(numpy.logical_and(signal[1:-1] < signal[:-2], signal[1:-1] < signal[2:]))

        # Return the changes
        return changes_left + changes_right

    def _filter_data_with_low_pass_filter(self, signal):
        """Filters an input sample/stroke data by a low-pass filter"""

        # Filter the signal
        signal.x = self.low_pass_filter.filter(signal.x)
        signal.y = self.low_pass_filter.filter(signal.y)
        signal.azimuth = self.low_pass_filter.filter(signal.azimuth)
        signal.tilt = self.low_pass_filter.filter(signal.tilt)
        signal.pressure = self.low_pass_filter.filter(signal.pressure)

        # Return the filtered signal
        return signal

    def _filter_data_with_gaussian_filter(self, signal):
        """Filters an input sample/stroke data by a Gaussian filter"""

        # Filter the signal
        signal.x = self.gaussian_filter.filter(signal.x)
        signal.y = self.gaussian_filter.filter(signal.y)
        signal.azimuth = self.gaussian_filter.filter(signal.azimuth)
        signal.tilt = self.gaussian_filter.filter(signal.tilt)
        signal.pressure = self.gaussian_filter.filter(signal.pressure)

        # Return the filtered signal
        return signal

    def _filter_velocity_with_low_pass_filter(self, velocity):
        """Filters an input velocity by a low-pass filter"""
        return self.low_pass_filter.filter(velocity)

    def _filter_velocity_with_gaussian_filter(self, velocity):
        """Filters an input velocity by a Gaussian filter"""
        return self.gaussian_filter.filter(velocity)
