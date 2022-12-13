import numpy
import functools
from handwriting_features.data.utils.math import intersection


class IntersectionUtils(object):
    """Class implementing intersection utils"""

    def __init__(self, sample_wrapper):
        """Initializes writing intersection object"""

        # Get the duration
        self.duration = sample_wrapper.sample_time[-1] - sample_wrapper.sample_time[0]

        # Get the on-surface strokes
        self.on_surface_strokes = sample_wrapper.on_surface_strokes

        # Set the number of intra-stroke intersections per stroke
        self.abs_num_intra = numpy.zeros((len(self.on_surface_strokes), 1), dtype=numpy.int)
        self.rel_num_intra = numpy.zeros((len(self.on_surface_strokes), 1), dtype=numpy.float)

        # Set the concatenated vector of strokes and intersections
        self.strokes_all_x = []
        self.strokes_all_y = []
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
        return 0 if not self.on_surface_strokes else self.num_inter

    def get_relative_number_of_inter_stroke_intersections(self):
        """Extracts the relative number of inter-stroke intersections"""
        return 0. if not self.on_surface_strokes else round(float(self.rel_num_inter), 6)

    @functools.lru_cache(maxsize=1)
    def _compute_intersections(self):
        """Computes the intra-stroke and inter-stroke intersections"""

        # Compute the intra-stroke intersections
        for i, stroke in enumerate(self.on_surface_strokes):
            intersections = [
                (x, y) for x, y in intersection(stroke.x, stroke.y)
                if x is not None and y is not None
            ]

            # Handle the intra-stroke intersections
            if intersections:
                self.abs_num_intra[i] = len(intersections)
                self.rel_num_intra[i] = len(intersections) / (stroke.time[-1] - stroke.time[0])
                self.intra_all.extend(intersections)

            # Add the stroke to the concatenated vector
            self.strokes_all_x.extend([x for x in stroke.x] + [numpy.nan])
            self.strokes_all_y.extend([y for y in stroke.y] + [numpy.nan])

        self.strokes_all_x = numpy.array(self.strokes_all_x)
        self.strokes_all_y = numpy.array(self.strokes_all_y)

        # Compute the inter-stroke intersections
        intersections = [
            (x, y) for x, y in intersection(self.strokes_all_x, self.strokes_all_y)
            if x is not None and y is not None
        ]

        # Handle the inter-stroke intersections
        if self.intra_all:
            intersections = [i for i in intersections if i not in self.intra_all]
        if intersections:
            self.num_inter = len(intersections)
            self.rel_num_inter = len(intersections) / self.duration
        else:
            self.num_inter = 0
            self.rel_num_inter = 0.
