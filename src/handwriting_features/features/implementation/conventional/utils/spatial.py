import numpy
import functools
from copy import deepcopy
from handwriting_features.data.utils.math import intersection
from handwriting_features.data.utils.math import derivation
from handwriting_features.data.utils.dsp import GaussianFilter, segment


class IntersectionUtils(object):
    """Class implementing intersection utils"""

    def __init__(self, sample_wrapper):
        """Initializes writing intersection object"""

        # Set the sample wrapper
        self.sample_wrapper = deepcopy(sample_wrapper)

        # Get the duration
        self.duration = self.sample_wrapper.sample_time[-1] - self.sample_wrapper.sample_time[0]

        # Get the on-surface strokes
        self.on_surface_strokes = self.sample_wrapper.on_surface_strokes

        # Set the number of intra-stroke and inter-stroke intersections per stroke
        self.abs_num_intra = numpy.zeros((len(self.on_surface_strokes), 1), dtype=int)
        self.rel_num_intra = numpy.zeros((len(self.on_surface_strokes), 1), dtype=float)
        self.abs_num_inter = 0
        self.rel_num_inter = 0.

        # Set the concatenated vector of strokes and intersections
        self.all_x = []
        self.all_y = []
        self.intra_all = []

        # Compute the intra-stroke and inter-stroke intersections
        self._compute_intersections()

    def get_number_of_intra_stroke_intersections(self):
        """Extracts the number of intra-stroke intersections"""
        return numpy.NaN if not self.on_surface_strokes else self.abs_num_intra.T

    def get_relative_number_of_intra_stroke_intersections(self):
        """Extracts the relative number of intra-stroke intersections"""
        return numpy.NaN if not self.on_surface_strokes else self.rel_num_intra.T

    def get_total_number_of_intra_stroke_intersections(self):
        """Extracts the total number of intra-stroke intersections"""
        return 0 if not self.on_surface_strokes else int(numpy.sum(self.abs_num_intra))

    def get_relative_total_number_of_intra_stroke_intersections(self):
        """Extracts the relative total number of intra-stroke intersections"""
        return 0. if not self.on_surface_strokes else round(float(numpy.sum(self.abs_num_intra) / self.duration), 6)

    def get_number_of_inter_stroke_intersections(self):
        """Extracts the number of inter-stroke intersections"""
        return 0 if not self.on_surface_strokes else self.abs_num_inter

    def get_relative_number_of_inter_stroke_intersections(self):
        """Extracts the relative number of inter-stroke intersections"""
        return 0. if not self.on_surface_strokes else round(float(self.rel_num_inter), 6)

    @functools.lru_cache(maxsize=1)
    def _compute_intersections(self):
        """Computes the intra-stroke and inter-stroke intersections"""

        # Compute the intra-stroke intersections
        for i, stroke in enumerate(self.on_surface_strokes):
            intersections = [(x, y) for x, y in intersection(stroke.x, stroke.y) if x is not None and y is not None]

            # Handle the intra-stroke intersections
            if intersections:
                self.abs_num_intra[i] = len(intersections)
                self.rel_num_intra[i] = len(intersections) / (stroke.time[-1] - stroke.time[0])
                self.intra_all.extend(intersections)

            # Add the stroke to the concatenated vector
            self.all_x.extend([x for x in stroke.x] + [numpy.nan])
            self.all_y.extend([y for y in stroke.y] + [numpy.nan])

        self.all_x = numpy.array(self.all_x)
        self.all_y = numpy.array(self.all_y)

        # Compute the inter-stroke intersections
        intersections = [(x, y) for x, y in intersection(self.all_x, self.all_y) if x is not None and y is not None]

        # Handle the inter-stroke intersections
        if self.intra_all:
            intersections = [i for i in intersections if i not in self.intra_all]
        if intersections:
            self.abs_num_inter = len(intersections)
            self.rel_num_inter = len(intersections) / self.duration
        else:
            self.abs_num_inter = 0
            self.rel_num_inter = 0.


class ProjectionUtils(object):
    """Class implementing projection utils"""

    # Default computational arguments
    n = 50

    def __init__(self, sample_wrapper, fs, n=None):
        """
        Initializes writing projection object.

        :param fs: sampling frequency
        :type fs: float
        :param n: number of samples of a Gaussian filter, defaults to 50
        :type n: int
        """

        # Set the sample wrapper
        self.sample_wrapper = deepcopy(sample_wrapper)

        # Set the on-surface data
        self.on_surface_data = self.sample_wrapper.on_surface_data

        # Set the DSP arguments
        self.fs = fs
        self.n = n if n else ProjectionUtils.n

        # Set the properties of the windowing function
        self.window_size = int(numpy.ceil(self.fs * 0.100))
        self.window_step = self.window_size

        # Set the filter instances
        self.gaussian_filter = GaussianFilter(self.fs, self.n)

        # Prepare time, peaks and valleys
        self.time = None
        self.peaks = None
        self.valleys = None

        # Compute the projections
        self._compute_projections()

    @functools.lru_cache(maxsize=1)
    def _compute_projections(self):
        """Computes the projections"""

        # Take time and vertical movement only
        t = self.on_surface_data.time
        y = self.on_surface_data.y

        # Segment time and vertical movement
        t_segmented = segment(t, self.window_size, self.window_step)
        y_segmented = segment(y, self.window_size, self.window_step)

        # Reshape the segments
        t_segmented = numpy.reshape(t_segmented, (t_segmented.shape[0], t_segmented.shape[-1])).T
        y_segmented = numpy.reshape(y_segmented, (y_segmented.shape[0], y_segmented.shape[-1])).T

        # Filter out segments with CV < 0.0001
        selection = (numpy.std(y_segmented, axis=0) / numpy.mean(y_segmented, axis=0)) > 0.0001
        t_segmented = t_segmented[:, selection]
        y_segmented = y_segmented[:, selection]

        # Flatten the segments to vectors
        t = t_segmented.flatten("F")
        y = y_segmented.flatten("F")

        # Filter vertical movement
        if len(y) > 3 * (self.n - 1):
            y_filtered = self.gaussian_filter.filter(y)
        else:
            y_filtered = numpy.array((y.tolist() + ([y[-1]] * len(y)))[:len(y)])

        # Compute the peaks and valleys
        peaks = numpy.array((y_filtered[1:-2] > y_filtered[0:-3]) & (y_filtered[1:-2] > y_filtered[2:-1]))
        valleys = numpy.array((y_filtered[1:-2] < y_filtered[0:-3]) & (y_filtered[1:-2] < y_filtered[2:-1]))

        # Set the time, peaks and valleys
        self.time = t
        self.peaks = numpy.array([i + 1 for i, p in enumerate(peaks) if p])
        self.valleys = numpy.array([i + 1 for i, p in enumerate(valleys) if p])

        # Adjust the peaks
        for i, peak in enumerate(self.peaks):
            while y[self.peaks[i]] < y[self.peaks[i] - 1] and y[self.peaks[i]] < y[self.peaks[i] + 1]:
                if y[self.peaks[i] - 1] > y[self.peaks[i] + 1]:
                    self.peaks[i] -= 1
                else:
                    self.peaks[i] += 1

        # Adjust the valleys
        for i, peak in enumerate(self.valleys):
            while y[self.valleys[i]] > y[self.valleys[i] - 1] and y[self.valleys[i]] > y[self.valleys[i] + 1]:
                if y[self.valleys[i] - 1] < y[self.valleys[i] + 1]:
                    self.valleys[i] -= 1
                else:
                    self.valleys[i] += 1

    @functools.lru_cache(maxsize=1)
    def _compute_temporal_velocity(self):
        """Computes the temporal velocity"""

        # Prepare the trajectory and time
        d = numpy.sqrt(derivation(self.on_surface_data.x) ** 2 + derivation(self.on_surface_data.y) ** 2)
        t = derivation(self.on_surface_data.time)

        # Return velocity
        return d / t

    @functools.lru_cache(maxsize=1)
    def vertical_peaks_indices(self):
        """Extracts the vertical peaks indices"""
        if all((self.time is not None, self.peaks is not None)):
            return numpy.array([numpy.where(self.on_surface_data.time == e)[0][0] for e in self.time[self.peaks]])
        else:
            return numpy.nan

    @functools.lru_cache(maxsize=1)
    def vertical_valleys_indices(self):
        """Extracts the vertical valleys indices"""
        if all((self.time is not None, self.valleys is not None)):
            return numpy.array([numpy.where(self.on_surface_data.time == e)[0][0] for e in self.time[self.valleys]])
        else:
            return numpy.nan

    def vertical_peaks_values(self):
        """Extracts the vertical peaks values"""
        if self.vertical_peaks_indices() is not numpy.nan:
            return numpy.array([self.on_surface_data.y[e] for e in self.vertical_peaks_indices()])
        else:
            return numpy.nan

    def vertical_valleys_values(self):
        """Extracts the vertical valleys values"""
        if self.vertical_valleys_indices() is not numpy.nan:
            return numpy.array([self.on_surface_data.y[e] for e in self.vertical_valleys_indices()])
        else:
            return numpy.nan

    def vertical_peaks_velocity(self):
        """Extracts the vertical peaks velocity"""
        if self.vertical_peaks_indices() is not numpy.nan:
            return numpy.array([self._compute_temporal_velocity()[e] for e in self.vertical_peaks_indices()])
        else:
            return numpy.nan

    def vertical_valleys_velocity(self):
        """Extracts the vertical valleys velocity"""
        if self.vertical_valleys_indices() is not numpy.nan:
            return numpy.array([self._compute_temporal_velocity()[e] for e in self.vertical_valleys_indices()])
        else:
            return numpy.nan

    def vertical_peaks_distance(self):
        """Extracts the vertical peaks distance"""
        if self.vertical_peaks_indices() is not numpy.nan and len(self.vertical_peaks_indices()) > 1:
            return derivation(numpy.array([self.on_surface_data.x[e] for e in self.vertical_peaks_indices()]))
        else:
            return numpy.nan

    def vertical_valleys_distance(self):
        """Extracts the vertical valleys distance"""
        if self.vertical_valleys_indices() is not numpy.nan and len(self.vertical_valleys_indices()) > 1:
            return derivation(numpy.array([self.on_surface_data.x[e] for e in self.vertical_valleys_indices()]))
        else:
            return numpy.nan

    def vertical_peaks_duration(self):
        """Extracts the vertical peaks duration"""
        if self.vertical_peaks_indices() is not numpy.nan and len(self.vertical_peaks_indices()) > 1:
            return derivation(numpy.array([self.on_surface_data.time[e] for e in self.vertical_peaks_indices()]))
        else:
            return numpy.nan

    def vertical_valleys_duration(self):
        """Extracts the vertical valleys duration"""
        if self.vertical_valleys_indices() is not numpy.nan and len(self.vertical_valleys_indices()) > 1:
            return derivation(numpy.array([self.on_surface_data.time[e] for e in self.vertical_valleys_indices()]))
        else:
            return numpy.nan
