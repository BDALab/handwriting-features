import numpy
from handwriting_features.features import HandwritingFeatures
from handwriting_features.features.configuration.mapping import HandwritingFeaturesMapping
from handwriting_features.features.validation import HandwritingFeaturesValidation
from handwriting_features.interface.featurizer.utils import SingleSubjectFeatureUtils, MultiSubjectFeatureUtils


class SingleSubjectFeatureExtractorHandler(object):
    """Class implementing the single-subject features extractor handler"""

    # Features
    features = HandwritingFeatures

    # Feature mapper
    mapping = HandwritingFeaturesMapping

    # Feature validator
    validation = HandwritingFeaturesValidation

    # Feature utils
    utils = SingleSubjectFeatureUtils

    @classmethod
    def extract(cls, data_values, data_labels=None, pipeline=None, **configuration):
        """
        Extracts the features specified in the pipeline for a single subject.

        :param data_values: sample values to extract the features from
        :type data_values: numpy.ndarray
        :param data_labels: labels for data samples, defaults to None
        :type data_labels: list, optional
        :param pipeline: pipeline of the features, defaults to None
        :type pipeline: list, optional
        :param configuration: common extractor configuration
        :type configuration: **kwargs
        :return: extracted features and labels
        :rtype: dict {"features": ..., "labels": ...}
        """

        # Initialize the handwriting features interface
        features = cls.features.from_numpy_array(data_values, data_labels, **configuration)

        # Initialize the feature mapping
        mapping = cls.mapping(features)

        # Prepare the buffers for extracted feature values/labels
        feature_values = []
        feature_labels = []

        # Extract the features specified in the features pipeline
        for feature in pipeline:

            # Get the validated feature arguments
            arguments = cls.validation.validate(feature.get("name"), feature.get("args"))

            # Extract the feature
            extracted = mapping.map(feature.get("name"))(**arguments)

            # Update the feature values/labels
            feature_values.append(cls.utils.prepare_feature_values(extracted))
            feature_labels.append(cls.utils.prepare_feature_labels(
                extracted,
                feature.get("name"),
                feature.get("args")))

        # Return the extracted feature values/labels
        return {
            "features": feature_values,
            "labels": feature_labels
        }


class MultiSubjectFeatureExtractorHandler(object):
    """Class implementing the multi-subject features extractor handler"""

    # Feature extractor
    extractor = SingleSubjectFeatureExtractorHandler

    # Feature utils
    utils = MultiSubjectFeatureUtils

    @classmethod
    def extract(cls, data_values, data_labels=None, pipeline=None, **configuration):
        """
        Extracts the features specified in the pipeline for multiple subjects.

        :param data_values: samples values to extract the features from
        :type data_values: numpy.ndarray
        :param data_labels: labels for data samples, defaults to None
        :type data_labels: list, optional
        :param pipeline: pipeline of the features, defaults to None
        :type pipeline: list, optional
        :param configuration: common extractor configuration
        :type configuration: **kwargs
        :return: extracted features and labels
        :rtype: dict {"features": ..., "labels": ...}
        """

        # Extract the features specified in the features pipeline for each subject
        extracted = [
            cls.extractor.extract(data_values[sample, ...], data_labels, pipeline, **configuration)
            for sample in range(data_values.shape[0])
        ]

        # Prepare the feature values/labels
        feature_values = cls.utils.prepare_feature_values(extracted, pipeline)
        feature_labels = cls.utils.prepare_feature_labels(extracted, pipeline)

        # Return the extracted feature values/labels
        return {
            "features": feature_values,
            "labels": feature_labels
        }
