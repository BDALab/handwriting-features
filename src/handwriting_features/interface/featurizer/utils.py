import numpy
from itertools import chain
from handwriting_features.features.configuration.settings import HandwritingFeaturesSettings


class SingleSubjectFeatureUtils(object):
    """Class implementing single-subject feature values/labels utils"""

    # Handwriting features settings
    features_settings = HandwritingFeaturesSettings

    @classmethod
    def prepare_feature_values(cls, extracted):
        """
        Prepares the feature values.

        :param extracted: extracted feature values
        :type extracted: numpy.ndarray
        :return: prepared feature values
        :rtype: numpy.ndarray
        """
        return extracted

    @classmethod
    def prepare_feature_labels(cls, extracted, feature_name, feature_args=None):
        """
        Prepares the feature labels.

        :param extracted: extracted feature values
        :type extracted: numpy.ndarray
        :param feature_name: feature name
        :type feature_name: str
        :param feature_args: feature arguments, defaults to None
        :type feature_args: dict, optional
        :return: prepared feature labels
        :rtype: list
        """

        # Prepare the base of the feature label(s) (handle these cases)
        #
        # 1. feature with statistics
        # 2. feature without statistics
        #    a) single-valued feature (i.e. no statistics are available)
        #    b) multi-valued (array-like) feature

        # Prepare default feature args
        feature_args = feature_args if feature_args else {}

        # 1. Handle: feature with statistics
        if feature_args.get("statistics"):

            # Prepare the feature label(s)
            statistics = feature_args["statistics"]
            statistics = [statistics] if isinstance(statistics, str) else statistics

            labels = [
                f"{stat}:{feature_name}"
                for stat in statistics
            ]

        # 2. Handle: feature without statistics
        else:

            # Prepare the feature label(s)
            labels = [f"{feature_name}"] * len(extracted)

            # Handle multi-values feature
            if len(labels) > 1:
                labels = [f"{label}(sample-{i})" for i, label in enumerate(labels, 1)]

        # Add the axis information
        if feature_args.get("axis"):
            if cls.features_settings.settings.get(feature_name, {}).get("arguments").get("axis"):
                labels = [
                    f"{label}:axis-{feature_args['axis']}"
                    for label in labels
                ]
        else:
            option = cls.features_settings.get_feature_argument_default(feature_name, "axis")
            labels = [f"{label}:axis-{option}" for label in labels] \
                if option is not None \
                else labels

        # Add the in-air/on-surface information
        if feature_args.get("in_air") is not None:
            if cls.features_settings.settings.get(feature_name, {}).get("arguments").get("in_air"):
                labels = [
                    f"{label}({'in-air' if feature_args['in_air'] else 'on-surface'})"
                    for label in labels
                ]
        else:
            option = cls.features_settings.get_feature_argument_default(feature_name, "in_air")
            labels = [f"{label}({'in-air' if option else 'on-surface'})" for label in labels] \
                if option is not None \
                else labels

        # Return the prepared feature labels
        return labels


class MultiSubjectFeatureUtils(object):
    """Class implementing multi-subject feature values/labels utils"""

    @classmethod
    def prepare_feature_values(cls, extracted, pipeline):
        """
        Prepares the feature values.

        :param extracted: extracted features
        :type extracted: list
        :param pipeline: pipeline of the features to be extracted
        :type pipeline: list
        :return: finalized feature values
        :rtype: numpy.ndarray
        """

        # Get the number of subjects and features
        num_subjects = len(extracted)
        num_features = len(pipeline)

        # Prepare the list of feature values (each feature with data for all subjects)
        features = [
            [subject["features"][feature] for subject in extracted]
            for feature in range(num_features)
        ]

        # Prepare the list of consolidated feature values
        consolidated = []

        # Consolidate the lengths of the feature values
        for feature in features:
            max_length = max(len(subject) for subject in feature)

            if all(len(subject) == max_length for subject in feature):
                consolidated.append(feature)
            else:
                consolidated.append([
                    numpy.concatenate([subject, numpy.full((max_length - len(subject),), numpy.nan)])
                    for subject in feature
                ])

        # Prepare the feature values to be finalized
        features = [
            [feature[subject] for feature in consolidated]
            for subject in range(num_subjects)
        ]

        # Finalize the feature values (concatenate: 1. over features. 2. over subjects)
        features = [numpy.expand_dims(numpy.hstack(subject), axis=0) for subject in features]
        features = numpy.vstack(list(subject for subject in features))

        # Return the finalized feature values
        return features

    @classmethod
    def prepare_feature_labels(cls, extracted, pipeline):
        """
        Prepares the feature labels.

        :param extracted: extracted features
        :type extracted: list
        :param pipeline: pipeline of the features to be extracted
        :type pipeline: list
        :return: finalized feature labels
        :rtype: list
        """

        # Get the number of features
        num_features = len(pipeline)

        # Prepare the list of feature labels (each feature with data for all subjects)
        features = [
            [subject["labels"][feature] for subject in extracted]
            for feature in range(num_features)
        ]

        # Finalize the feature labels
        labels = list(chain.from_iterable([max(feature, key=len) for feature in features]))

        # Return the finalized feature labels
        return labels
