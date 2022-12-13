from handwriting_features.features.base import HandwritingFeaturesBase
from handwriting_features.features.implementation import *


class HandwritingFeatures(HandwritingFeaturesBase):
    """Class implementing interface for computation of handwriting features"""

    # -------------------- #
    # Handwriting features #
    # -------------------- #

    # ---------------------
    # 1. Kinematic features

    def velocity(self, axis="xy", in_air=False, statistics=()):
        """
        Extracts the velocity.

        :param axis: axis to compute the velocity from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: velocity
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, velocity, statistics=statistics, axis=axis, in_air=in_air)

    def acceleration(self, axis="xy", in_air=False, statistics=()):
        """
        Extracts the acceleration.

        :param axis: axis to compute the acceleration from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: acceleration
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, acceleration, statistics=statistics, axis=axis, in_air=in_air)

    def jerk(self, axis="xy", in_air=False, statistics=()):
        """
        Extracts the jerk.

        :param axis: axis to compute the jerk from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: jerk
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, jerk, statistics=statistics, axis=axis, in_air=in_air)

    # -------------------
    # 2. Dynamic features

    def azimuth(self, in_air=False, statistics=()):
        """
        Extracts the azimuth.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: azimuth
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, azimuth, statistics=statistics, in_air=in_air)

    def tilt(self, in_air=False, statistics=()):
        """
        Extracts the tilt.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: tilt
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, tilt, statistics=statistics, in_air=in_air)

    def pressure(self, statistics=()):
        """
        Extracts the pressure.

        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: pressure
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, pressure, statistics=statistics)

    # -------------------
    # 3. Spatial features

    def stroke_length(self, in_air=False, statistics=()):
        """
        Extracts the stroke length.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: stroke length
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, stroke_length, statistics=statistics, in_air=in_air)

    def stroke_height(self, in_air=False, statistics=()):
        """
        Extracts the stroke height.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: stroke height
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, stroke_height, statistics=statistics, in_air=in_air)

    def stroke_width(self, in_air=False, statistics=()):
        """
        Extracts the stroke width.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: stroke width
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, stroke_width, statistics=statistics, in_air=in_air)

    def writing_length(self, in_air=False):
        """
        Extracts the writing length.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: writing length
        :rtype: float
        """
        return self.compute(self.wrapper, writing_length, in_air=in_air)

    def writing_height(self, in_air=False):
        """
        Extracts the writing height.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: writing height
        :rtype: float
        """
        return self.compute(self.wrapper, writing_height, in_air=in_air)

    def writing_width(self, in_air=False):
        """
        Extracts the writing width.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: writing width
        :rtype: float
        """
        return self.compute(self.wrapper, writing_width, in_air=in_air)

    def number_of_intra_stroke_intersections(self, statistics=()):
        """
        Extracts the number of intra-stroke intersections.

        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: number of intra-stroke intersections
        :rtype: numpy.ndarray or np.NaN
        """
        return self.compute(self.wrapper, number_of_intra_stroke_intersections, statistics=statistics)

    def relative_number_of_intra_stroke_intersections(self, statistics=()):
        """
        Extracts the relative number of intra-stroke intersections.

        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: relative number of intra-stroke intersections
        :rtype: numpy.ndarray or np.NaN
        """
        return self.compute(self.wrapper, relative_number_of_intra_stroke_intersections, statistics=statistics)

    def total_number_of_intra_stroke_intersections(self):
        """
        Extracts the total number of intra-stroke intersections.

        :return: total number of intra-stroke intersections
        :rtype: int
        """
        return self.compute(self.wrapper, total_number_of_intra_stroke_intersections)

    def relative_total_number_of_intra_stroke_intersections(self):
        """
        Extracts the relative total number of intra-stroke intersections.

        :return: relative total number of intra-stroke intersections
        :rtype: float
        """
        return self.compute(self.wrapper, relative_total_number_of_intra_stroke_intersections)

    def number_of_inter_stroke_intersections(self):
        """
        Extracts the number of inter-stroke intersections.

        :return: number of inter-stroke intersections
        :rtype: int
        """
        return self.compute(self.wrapper, number_of_inter_stroke_intersections)

    def relative_number_of_inter_stroke_intersections(self):
        """
        Extracts the relative number of inter-stroke intersections.

        :return: relative number of inter-stroke intersections
        :rtype: float
        """
        return self.compute(self.wrapper, relative_number_of_inter_stroke_intersections)

    # --------------------
    # 4. Temporal features

    def stroke_duration(self, in_air=False, statistics=()):
        """
        Extracts the stroke duration.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: stroke duration
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, stroke_duration, statistics=statistics, in_air=in_air)

    def ratio_of_stroke_durations(self, statistics=()):
        """
        Extracts the ratio of stroke durations: on-surface / in-air.

        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: ratio of stroke durations
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.compute(self.wrapper, ratio_of_stroke_durations, statistics=statistics)

    def writing_duration(self, in_air=False):
        """
        Extracts the writing duration.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: writing duration
        :rtype: float
        """
        return self.compute(self.wrapper, writing_duration, in_air=in_air)

    def writing_duration_overall(self):
        """
        Extracts the overall writing duration.

        :return: overall writing duration
        :rtype: float
        """
        return self.compute(self.wrapper, writing_duration_overall)

    def ratio_of_writing_durations(self):
        """
        Extracts the ratio of writing durations: on-surface / in-air.

        :return: ratio of writing durations
        :rtype: float
        """
        return self.compute(self.wrapper, ratio_of_writing_durations)

    def number_of_interruptions(self):
        """
        Extracts the number of interruptions.

        :return: number of interruptions
        :rtype: float
        """
        return self.compute(self.wrapper, number_of_interruptions)

    def number_of_interruptions_relative(self):
        """
        Extracts the number of interruptions relative to the duration.

        :return: number of interruptions relative to the duration
        :rtype: float
        """
        return self.compute(self.wrapper, number_of_interruptions_relative)

    # ---------------------
    # 5. Composite features

    def writing_tempo(self, in_air=False):
        """
        Extracts the writing tempo.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: writing tempo
        :rtype: float
        """
        return self.compute(self.wrapper, writing_tempo, in_air=in_air)

    def writing_stops(self, statistics=()):
        """
        Extracts the writing stops.

        :param statistics: statistics to compute, defaults to ()
        :type statistics: Any[list, tuple], optional
        :return: writing stops
        :rtype: numpy.ndarray or np.NaN
        """
        return self.compute(self.wrapper, writing_stops, statistics=statistics)

    def writing_number_of_changes(self, fs, fc=None, n=None):
        """
        Extracts the number of writing changes.

        :param fs: sampling frequency
        :type fs: float
        :param fc: cutoff frequency for the low-pass filter, defaults to None
        :type fc: float, optional
        :param n: number of samples of a Gaussian filter, defaults to None
        :type n: int
        :return: number of writing changes
        :rtype: numpy.ndarray or np.NaN
        """
        return self.compute(self.wrapper, writing_number_of_changes, fs=fs, fc=fc, n=n)
