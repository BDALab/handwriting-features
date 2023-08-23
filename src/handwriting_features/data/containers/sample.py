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

    def __init__(self, sample, source=None):
        """Constructor method"""

        # Set the sample
        self.sample = sample
        self.source = source

        # Set the strokes
        self.strokes = self.sample.get_strokes()

    def __str__(self):
        return f"{self.source}" if self.source else f"HandwritingSampleWrapper({self.sample})"

    def __repr__(self):
        return self.__str__()

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
        return cls(HandwritingSample.from_json(path, labels), path)

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
        return cls(HandwritingSample.from_svc(path, labels), path)

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

        # Compute the velocity
        velocity = numpy.concatenate(self._compute_strokes_velocities(axis, in_air))

        # Return the velocity
        return velocity if velocity is not None and velocity.size > 0 else numpy.nan

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

        # Compute the acceleration
        acceleration = numpy.concatenate(self._compute_strokes_accelerations(axis, in_air))

        # Return the acceleration
        return acceleration if acceleration is not None and acceleration.size > 0 else numpy.nan

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

        # Compute the jerk
        jerk = numpy.concatenate(self._compute_strokes_jerks(axis, in_air))

        # Return the jerk
        return jerk if jerk is not None and jerk.size > 0 else numpy.nan

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
        data = self.on_surface_data if not in_air else self.in_air_data

        # Return the azimuth
        return data.azimuth

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
        data = self.on_surface_data if not in_air else self.in_air_data

        # Return the tilt
        return data.tilt

    @functools.lru_cache(maxsize=1)
    def compute_pressure(self):
        """
        Computes the pressure.

        :return: tilt
        :rtype: numpy.ndarray or numpy.NaN
        """
        return self.on_surface_data.pressure

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

    @functools.cached_property
    def in_air_data(self):
        return self.sample.get_in_air_data()

    @functools.cached_property
    def on_surface_data(self):
        return self.sample.get_on_surface_data()

    @functools.cached_property
    def in_air_strokes(self):
        return [stroke for status, stroke in self.strokes if status == "in_air"]

    @functools.cached_property
    def on_surface_strokes(self):
        return [stroke for status, stroke in self.strokes if status == "on_surface"]

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

    # ---------------------- #
    # Computational routines #
    # ---------------------- #

    @functools.lru_cache(maxsize=len(axes) * len(surfaces))
    def _compute_strokes_trajectories(self, axis="xy", in_air=False):
        """
        Computes the strokes trajectories.

        :param axis: axis to compute the trajectories from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: strokes trajectories
        :rtype: list
        """

        # Get the strokes
        strokes = self.on_surface_strokes if not in_air else self.in_air_strokes

        # Return the strokes trajectories
        if axis == "x":
            return [numpy.abs(derivation(stroke.x)) for stroke in strokes]
        if axis == "y":
            return [numpy.abs(derivation(stroke.y)) for stroke in strokes]
        if axis == "xy":
            return [
                numpy.sqrt(numpy.power(derivation(stroke.x), 2) + numpy.power(derivation(stroke.y), 2))
                for stroke in strokes
            ]

    @functools.lru_cache(maxsize=len(surfaces))
    def _compute_strokes_time_differences(self, in_air=False):
        """
        Computes the strokes time differences.

        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: strokes time differences
        :rtype: list
        """
        return [
            derivation(stroke.time)
            for stroke in (self.on_surface_strokes if not in_air else self.in_air_strokes)
        ]

    @functools.lru_cache(maxsize=len(axes) * len(surfaces))
    def _compute_strokes_velocities(self, axis="xy", in_air=False):
        """
        Computes the strokes velocities.

        :param axis: axis to compute the velocities from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: strokes velocities
        :rtype: list
        """

        # Get the variable to differentiate over (strokes trajectories)
        ds = self._compute_strokes_trajectories(axis, in_air)

        # Get the stroke time differences
        dt = self._compute_strokes_time_differences(in_air)

        # Return the stokes velocities
        return [d / t for (d, t) in zip(ds, dt)]

    @functools.lru_cache(maxsize=len(axes) * len(surfaces))
    def _compute_strokes_accelerations(self, axis="xy", in_air=False):
        """
        Computes the strokes accelerations.

        :param axis: axis to compute the accelerations from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: strokes accelerations
        :rtype: list
        """

        # Get the variable to differentiate over (strokes velocities)
        dv = self._compute_strokes_velocities(axis, in_air)

        # Get the stroke time differences
        dt = self._compute_strokes_time_differences(in_air)

        # Return the stokes accelerations
        return [derivation(d) / t[1:] for (d, t) in zip(dv, dt)]

    @functools.lru_cache(maxsize=len(axes) * len(surfaces))
    def _compute_strokes_jerks(self, axis="xy", in_air=False):
        """
        Computes the strokes jerks.

        :param axis: axis to compute the jerks from, defaults to "xy"
        :type axis: str, optional
        :param in_air: in-air flag, defaults to False
        :type in_air: bool, optional
        :return: strokes jerks
        :rtype: list
        """

        # Get the variable to differentiate over (strokes accelerations)
        da = self._compute_strokes_accelerations(axis, in_air)

        # Get the stroke time differences
        dt = self._compute_strokes_time_differences(in_air)

        # Return the stokes jerks
        return [derivation(d) / t[2:] for (d, t) in zip(da, dt)]
