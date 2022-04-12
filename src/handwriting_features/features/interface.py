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

    def writing_tempo(self, in_air=False):
        """
        Extracts the writing tempo.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: writing tempo
        :rtype: float
        """
        return self.compute(self.wrapper, writing_tempo, in_air=in_air)

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
