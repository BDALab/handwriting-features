import numpy
from handwriting_features.features import HandwritingFeatures
from handwriting_features.features.configuration.mapping import HandwritingFeaturesMapping
from handwriting_features.features.validation import HandwritingFeaturesFusion, HandwritingFeaturesValidation
from handwriting_features.interface.featurizer.utils import (
    SingleSubjectFeatureUtils,
    MultiSubjectFeatureUtils,
    FeaturesPipelineUtils
)


class BaseFeatureExtractorHandler(object):
    """Base class for the feature extractor handlers"""

    # Features pipeline utils
    pipeline_utils = FeaturesPipelineUtils

    # Features
    features = HandwritingFeatures

    # Feature mapper
    mapping = HandwritingFeaturesMapping

    # Feature validator
    validation = HandwritingFeaturesValidation


class SingleSubjectFeatureExtractorHandler(BaseFeatureExtractorHandler):
    """Class implementing the single-subject features extractor handler"""

    # Feature utils
    utils = SingleSubjectFeatureUtils

    @classmethod
    def extract(cls, data_values, data_labels=None, pipeline=None, preparation=True, **configuration):
        """
        Extracts the features specified in the pipeline for a single subject.

        :param data_values: sample values to extract the features from
        :type data_values: numpy.ndarray
        :param data_labels: labels for data samples, defaults to None
        :type data_labels: list, optional
        :param pipeline: pipeline of the features, defaults to None
        :type pipeline: list, optional
        :param preparation: prepare the pipeline of features, defaults to True
        :type preparation: bool, optional
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

        # Prepare the features pipeline
        if preparation:
            pipeline = cls.pipeline_utils.prepare_features_pipeline(pipeline)

        # Extract the features specified in the features pipeline
        for feature in pipeline:

            # Get the feature name and args
            name = feature.get("name")
            args = feature.get("args", {})

            # Prepare the feature args (fuze the feature args with the common configuration)
            args = HandwritingFeaturesFusion.fuze(
                feature.get("name"),
                args,
                features.config,
                features.skip_features)

            # Get the validated feature arguments
            arguments = cls.validation.validate(name, args)

            # Extract the feature
            extracted = mapping.map(feature.get("name"))(**arguments)

            # Update the feature values/labels
            feature_values.append(cls.utils.prepare_feature_values(extracted))
            feature_labels.append(cls.utils.prepare_feature_labels(extracted, name, args))

        # Return the extracted feature values/labels
        return {
            "features": feature_values,
            "labels": feature_labels
        }


class MultiSubjectFeatureExtractorHandler(BaseFeatureExtractorHandler):
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

        # Prepare the features pipeline
        pipeline = cls.pipeline_utils.prepare_features_pipeline(pipeline)

        # Extract the features specified in the features pipeline for each subject
        extracted = [
            cls.extractor.extract(
                data_values=data_values[sample, ...],
                data_labels=data_labels,
                pipeline=pipeline,
                preparation=False,
                **configuration)
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
