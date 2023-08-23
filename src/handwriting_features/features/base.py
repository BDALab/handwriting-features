import sys
import logging
import numpy
from handwriting_features.features.configuration.settings import HandwritingFeaturesSettings
from handwriting_features.data.descriptors.statistics import Statistics
from handwriting_features.data.containers.sample import HandwritingSampleWrapper
from handwriting_features.features.validation import HandwritingFeaturesFusion, HandwritingFeaturesValidation


# Set the logging configuration
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("FeatureExtractor")


class HandwritingFeaturesBase(object):
    """Base class for handwriting features"""

    def __init__(self, sample_wrapper, **config):
        """Constructor method"""

        # Set the sample and the extractor configuration
        self.wrapper = sample_wrapper
        self.config = config if config else {}

        # Set the features to be skipped during preparation
        self.skip_features = self.config.pop("skip_features", ("statistics", ))

        # Set the logging
        self.logging_settings = self.config.pop("logging_settings", {})

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
    def inject_common_configuration(cls, method, kwargs, common, skip_features=None):
        """
        Injects the common configuration into the kwargs.

        :param method: feature computation method to be applied
        :type method: callable
        :param kwargs: feature computation-specific kwargs
        :type kwargs: dict
        :param skip_features: features to be skipped during injection, defaults to None
        :type skip_features: Any[list, tuple], optional
        :param common: common configuration
        :type common: dict
        :return: kwargs
        :rtype: dict
        """
        return HandwritingFeaturesFusion.fuze(method.__name__, kwargs, common, skip_features)

    @classmethod
    def before_computation(cls, method, kwargs=None, skip_features=None):
        """
        Applies the before-computation hook.

        :param method: feature computation method to be applied
        :type method: callable
        :param kwargs: feature computation-specific kwargs
        :type kwargs: dict
        :param skip_features: features to be skipped during validation, defaults to None
        :type skip_features: Any[list, tuple], optional
        :return: kwargs
        :rtype: dict
        """
        return HandwritingFeaturesValidation.validate(method.__name__, kwargs, skip_features)

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

    def compute(self, sample_wrapper, method, statistics=None, **kwargs):
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

        # Prepare the method name
        method_name = method.__name__

        # Prepare the configuration
        settings = self.inject_common_configuration(method, kwargs, self.config, self.skip_features)

        # Apply the before-computation hook
        settings = self.before_computation(method, settings, self.skip_features)

        # Apply the computation
        try:
            features = method(sample_wrapper, **settings)
        except Exception as e:
            if self.logging_settings.get("soft_validation"):
                logger.warning(f"Failure '{method_name}' for {sample_wrapper}: {e.__class__.__name__} - {e}")
                if HandwritingFeaturesSettings.is_feature_multivalued(method_name):
                    features = numpy.array([])
                else:
                    features = numpy.nan
            else:
                raise e

        # Apply the after-computation hook
        features = self.after_computation(features, statistics)

        # Return the features
        return features
