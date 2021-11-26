import numpy
import functools
from handwriting_sample import HandwritingSample
from handwriting_features.data.utils.math import derivation
from handwriting_features.data.exceptions.sample import *


class HandwritingSampleWrapper(object):
    """Class implementing the handwriting sample wrapper"""

    # Handwriting data axes
    axes = ("x", "y", "xy")

    # Handwriting data surface information
    surfaces = ("on_surface", "in_air")

    def __init__(self, sample):
        """Constructor method"""
        self.sample = sample

    # ------------------------------- #
    # Alternative constructor methods #
    # ------------------------------- #

    @classmethod
    def from_list(cls, values, labels=None):
        """
        Initializes HandwritingSampleWrapper object from a list.

        :param values: data values
        :type values: list
        :param labels: labels for the data values
        :type labels: list, optional
        :return: HandwritingSampleWrapper object
        :rtype: HandwritingSampleWrapper
        """
        return cls(HandwritingSample.from_list(values, labels))

    @classmethod
    def from_numpy_array(cls, values, labels=None):
        """
        Initializes HandwritingSampleWrapper object from a numpy array.

        :param values: data values
        :type values: numpy.ndarray
        :param labels: labels for the data values
        :type labels: list, optional
        :return: HandwritingSampleWrapper object
        :rtype: HandwritingSampleWrapper
        """
        return cls(HandwritingSample.from_numpy_array(values, labels))

    @classmethod
    def from_pandas_dataframe(cls, values, labels=None):
        """
        Initializes HandwritingSampleWrapper object from a pandas DataFrame.

        :param values: data values
        :type values: pandas.DataFrame
        :param labels: labels for the data values
        :type labels: list, optional
        :return: HandwritingSampleWrapper object
        :rtype: HandwritingSampleWrapper
        """
        return cls(HandwritingSample.from_pandas_dataframe(values, labels))

    @classmethod
    def from_json(cls, path, labels=None):
        """
        Initializes HandwritingSampleWrapper object from a JSON file.

        :param path: path to a JSON file
        :type path: str
        :param labels: labels for the data values
        :type labels: list, optional
        :return: HandwritingSampleWrapper object
        :rtype: HandwritingSampleWrapper
        """
        return cls(HandwritingSample.from_json(path, labels))

    @classmethod
    def from_svc(cls, path, labels=None):
        """
        Initializes HandwritingSampleWrapper object from an SVC file.

        :param path: path to an SVC file
        :type path: str
        :param labels: labels for the data values
        :type labels: list, optional
        :return: HandwritingSampleWrapper object
        :rtype: HandwritingSampleWrapper
        """
        return cls(HandwritingSample.from_svc(path, labels))

    # ----------------------------- #
    # Derived handwriting variables #
    # ----------------------------- #

    @functools.lru_cache(maxsize=len(axes) * len(surfaces))
    def compute_velocity(self, axis="xy", in_air=False):
        """
        Computes the velocity.

        :param axis: axis to compute the velocity from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: velocity
        :rtype: numpy.ndarray or numpy.NaN
        """

        # Validate the input arguments
        self.validate_axis(axis)
        self.validate_surface_movement(in_air)

        # Get the data to be used for the feature computation
        data = self.sample.get_on_surface_strokes() if not in_air else self.sample.get_in_air_strokes()

        # Compute velocity for each stroke separately
        velocity = [
            derivation(stroke.xy if axis == "xy" else (stroke.x if axis == "x" else stroke.y))
            for _, stroke in data
        ]

        # Assemble the velocity from the strokes
        velocity = numpy.concatenate(velocity) if velocity else numpy.nan

        # Return the velocity
        return velocity

    @functools.lru_cache(maxsize=len(axes) * len(surfaces))
    def compute_acceleration(self, axis="xy", in_air=False):
        """
        Computes the acceleration.

        :param axis: axis to compute the acceleration from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: acceleration
        :rtype: numpy.ndarray or numpy.NaN
        """

        # Validate the input arguments
        self.validate_axis(axis)
        self.validate_surface_movement(in_air)

        # Return the acceleration
        return derivation(self.compute_velocity(axis, in_air))

    @functools.lru_cache(maxsize=len(axes) * len(surfaces))
    def compute_jerk(self, axis="xy", in_air=False):
        """
        Computes the jerk.

        :param axis: axis to compute the jerk from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: jerk
        :rtype: numpy.ndarray or numpy.NaN
        """

        # Validate the input arguments
        self.validate_axis(axis)
        self.validate_surface_movement(in_air)

        # Return the jerk
        return derivation(self.compute_acceleration(axis, in_air))

    @functools.lru_cache(maxsize=len(surfaces))
    def compute_azimuth(self, in_air=False):
        """
        Computes the azimuth.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: azimuth
        :rtype: numpy.ndarray or numpy.NaN
        """

        # Validate the input arguments
        self.validate_surface_movement(in_air)

        # Get the data to be used for the feature computation
        data = self.sample.get_on_surface_data() if not in_air else self.sample.get_in_air_data()
        data = data.azimuth

        # Return the azimuth
        return data

    @functools.lru_cache(maxsize=len(surfaces))
    def compute_tilt(self, in_air=False):
        """
        Computes the tilt.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: tilt
        :rtype: numpy.ndarray or numpy.NaN
        """

        # Validate the input arguments
        self.validate_surface_movement(in_air)

        # Get the data to be used for the feature computation
        data = self.sample.get_on_surface_data() if not in_air else self.sample.get_in_air_data()
        data = data.tilt

        # Return the tilt
        return data

    # ---------------------------- #
    # Sample handwriting variables #
    # ---------------------------- #

    @property
    def sample_x(self):
        return self.sample.x

    @property
    def sample_y(self):
        return self.sample.y

    @property
    def sample_time(self):
        return self.sample.time

    @property
    def sample_pen_status(self):
        return self.sample.pen_status

    @property
    def sample_azimuth(self):
        return self.sample.azimuth

    @property
    def sample_tilt(self):
        return self.sample.tilt

    @property
    def sample_pressure(self):
        return self.sample.pressure

    # ------------------- #
    # Validation routines #
    # ------------------- #

    @classmethod
    def validate_axis(cls, axis):
        """Validates the axis"""
        if axis not in cls.axes:
            raise UnsupportedAxisError(f"Unsupported <axis> argument {axis}; must be in {cls.axes}")

    @classmethod
    def validate_surface_movement(cls, in_air):
        """Validates the surface movement"""
        if not isinstance(in_air, bool):
            raise UnsupportedSurfaceMovementError(f"Unsupported <in_air> argument {in_air}; must be bool")
