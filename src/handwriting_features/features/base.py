import numpy
from handwriting_features.data.descriptors.statistics import Statistics
from handwriting_features.data.containers.sample import HandwritingSampleWrapper
from handwriting_features.features.validation import HandwritingFeaturesValidation


class HandwritingFeaturesBase(object):
    """Base class for handwriting features"""

    def __init__(self, sample_wrapper, **config):
        """Constructor method"""

        # Set the sample and the extractor configuration
        self.wrapper = sample_wrapper
        self.config = config if config else {}

    # ------------------------------- #
    # Alternative constructor methods #
    # ------------------------------- #

    @classmethod
    def from_sample(cls, sample, **config):
        """
        Initializes HandwritingFeatures object from a sample.
        :param sample: handwriting sample object
        :type sample: HandwritingSample
        :param config: common configuration
        :type config: **kwargs
        :return: HandwritingFeatures object
        :rtype: HandwritingFeatures
        """
        return cls(HandwritingSampleWrapper(sample), **config)

    @classmethod
    def from_list(cls, values, labels=None, **config):
        """
        Initializes HandwritingFeatures object from a list.

        :param values: data values
        :type values: list
        :param labels: labels for the data values
        :type labels: list, optional
        :param config: common configuration
        :type config: **kwargs
        :return: HandwritingFeatures object
        :rtype: HandwritingFeatures
        """
        return cls(HandwritingSampleWrapper.from_list(values, labels), **config)

    @classmethod
    def from_numpy_array(cls, values, labels=None, **config):
        """
        Initializes HandwritingFeatures object from a numpy array.

        :param values: data values
        :type values: numpy.ndarray
        :param labels: labels for the data values
        :type labels: list, optional
        :param config: common configuration
        :type config: **kwargs
        :return: HandwritingFeatures object
        :rtype: HandwritingFeatures
        """
        return cls(HandwritingSampleWrapper.from_numpy_array(values, labels), **config)

    @classmethod
    def from_pandas_dataframe(cls, values, labels=None, **config):
        """
        Initializes HandwritingFeatures object from a pandas DataFrame.

        :param values: data values
        :type values: pandas.DataFrame
        :param labels: labels for the data values
        :type labels: list, optional
        :param config: common configuration
        :type config: **kwargs
        :return: HandwritingFeatures object
        :rtype: HandwritingFeatures
        """
        return cls(HandwritingSampleWrapper.from_pandas_dataframe(values, labels), **config)

    @classmethod
    def from_json(cls, path, labels=None, **config):
        """
        Initializes HandwritingFeatures object from a JSON file.

        :param path: path to a JSON file
        :type path: str
        :param labels: labels for the data values
        :type labels: list, optional
        :param config: common configuration
        :type config: **kwargs
        :return: HandwritingFeatures object
        :rtype: HandwritingFeatures
        """
        return cls(HandwritingSampleWrapper.from_json(path, labels), **config)

    @classmethod
    def from_svc(cls, path, labels=None, **config):
        """
        Initializes HandwritingFeatures object from an SVC file.

        :param path: path to an SVC file
        :type path: str
        :param labels: labels for the data values
        :type labels: list, optional
        :param config: common configuration
        :type config: **kwargs
        :return: HandwritingFeatures object
        :rtype: HandwritingFeatures
        """
        return cls(HandwritingSampleWrapper.from_svc(path, labels), **config)

    # ----------------- #
    # Computation hooks #
    # ----------------- #

    @classmethod
    def before_computation(cls, method, kwargs=None):
        """
        Applies the before-computation hook.

        :param method: feature computation method to be applied
        :type method: callable
        :param kwargs: feature computation-specific kwargs
        :type kwargs: dict
        :return: kwargs
        :rtype: dict
        """
        return HandwritingFeaturesValidation.validate(method.__name__, kwargs, ("statistics", ))

    @classmethod
    def after_computation(cls, feature, statistics=None):
        """
        Applies the after-computation hook.

        :param feature: computed feature
        :type feature: numpy.ndarray
        :param statistics: statistics to be computed, defaults to None
        :type statistics: Any[str, list, tuple], optional
        :return: features
        :rtype: numpy.ndarray
        """

        # Handle the statistics options
        statistics = [statistics] if isinstance(statistics, str) else statistics

        # Compute the statistics
        if statistics:
            feature = numpy.array([Statistics.compute(feature, stat) for stat in statistics])
        else:
            if not isinstance(feature, numpy.ndarray):
                feature = numpy.array(feature).reshape((1,))

        # Return the feature
        return feature

    @classmethod
    def compute(cls, sample_wrapper, method, statistics=None, **kwargs):
        """
        Applies the computation (including before-after computational hooks).

        :param sample_wrapper: sample wrapper object
        :type sample_wrapper: HandwritingSampleWrapper
        :param method: feature computation method to be applied
        :type method: callable
        :param statistics: statistics to be computed, defaults to None
        :type statistics: iterable, optional
        :param kwargs: feature computation-specific kwargs
        :type kwargs: **kwargs
        :return: computed features
        :rtype: numpy.ndarray
        """

        # Apply the before-computation hook
        kwargs = cls.before_computation(method, kwargs)

        # Apply the computation
        features = method(sample_wrapper, **kwargs)

        # Apply the after-computation hook
        features = cls.after_computation(features, statistics)

        # Return the features
        return features
