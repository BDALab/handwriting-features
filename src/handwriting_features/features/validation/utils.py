from handwriting_features.features.exceptions.validation import *
from handwriting_features.features.configuration.settings import HandwritingFeaturesSettings


class HandwritingFeaturesFusion(object):
    """Class implementing the handwriting features fusion"""

    # Handwriting features settings
    features_settings = HandwritingFeaturesSettings.settings

    @classmethod
    def fuze(cls, feature_name, feature_args=None, common_configuration=None, skip_features=()):
        """
        Fuze the feature arguments with the common configuration.

        :param feature_name: feature name
        :type feature_name: str
        :param feature_args: feature arguments, defaults to None
        :type feature_args: dict, optional
        :param common_configuration: common configuration, defaults to None
        :type common_configuration: dict, optional
        :param skip_features: skip preparation for args names (features), defaults to ()
        :type skip_features: Any[list, tuple], optional
        :return: updated feature arguments
        :rtype: dict
        """

        # Prepare default feature args
        feature_args = feature_args if feature_args else {}

        # Get the features in the feature's configuration (to be used and configured)
        features_in_configuration = HandwritingFeaturesSettings.get_feature_arguments(feature_name).keys()

        # Update the feature arguments with the common configuration
        if common_configuration:
            for key, value in common_configuration.items():
                if key in feature_args:
                    continue
                if key in skip_features:
                    continue
                if value is None:
                    continue
                if key in features_in_configuration:
                    feature_args[key] = value

        # Return the updated feature arguments
        return feature_args


class HandwritingFeaturesValidation(object):
    """Class implementing the handwriting features validation"""

    # Handwriting features settings
    features_settings = HandwritingFeaturesSettings.settings

    @classmethod
    def validate(cls, feature_name, feature_args=None, skip_features=()):
        """
        Validate the feature arguments.

        :param feature_name: feature name
        :type feature_name: str
        :param feature_args: feature arguments, defaults to None
        :type feature_args: dict, optional
        :param skip_features: skip validation for args names (features), defaults to ()
        :type skip_features: Any[list, tuple], optional
        :return: validated feature arguments
        :rtype: dict
        """

        # Check the feature
        #
        # 1. check if the feature name is provided
        # 2. check if the type of feature name
        # 3. check if the feature name is known
        # 4. check if there are any arguments for the feature
        if not feature_name:
            raise FeatureNameMissingError("Missing feature name")
        if not isinstance(feature_name, str):
            raise FeatureNameInvalidTypeError(f"Unsupported feature type: {feature_name}")
        if feature_name not in cls.features_settings:
            raise FeatureNameUnsupportedError(f"Unsupported feature: {feature_name}")
        if not cls.features_settings.get(feature_name):
            return {}

        # Prepare default feature args
        feature_args = feature_args if feature_args else {}

        # Prepare the validated arguments
        validated_args = {}

        # ------------------------------- #
        # Validate the feature properties #
        # ------------------------------- #

        # 1. Validate the applicability of the statistical functions
        if not cls.features_settings.get(feature_name).get("properties").get("is_multi_valued"):
            if feature_args.get("statistics") and feature_args["statistics"]:
                raise StatisticsForSingleValuedFeatureError(
                    f"No statistics supported for single-valued features. "
                    f"feature: {feature_name}")

        # ------------------------------ #
        # Validate the feature arguments #
        # ------------------------------ #

        for argument_name, argument_settings in cls.features_settings.get(feature_name).get("arguments").items():

            # Handle skip validation
            if skip_features and argument_name in skip_features:
                continue

            # Get the argument data and type
            arg_data = feature_args.get(argument_name)
            arg_type = type(arg_data)

            # If the feature is optional, try to use a default value (if available)
            if not argument_settings.get("mandatory"):
                if arg_data is None and argument_settings.get("default"):
                    validated_args[argument_name] = argument_settings.get("default")

            # 1. Validate the presence of the mandatory argument
            if argument_name not in feature_args:
                if argument_settings.get("mandatory"):
                    raise FeatureArgumentMissingError(
                        f"Missing argument mandatory feature argument. "
                        f"argument name: {argument_name}, "
                        f"feature: {feature_name}")
                else:
                    continue

            # 2. Validate the type of the argument
            if argument_settings.get("type"):
                if arg_type not in argument_settings.get("type"):
                    raise FeatureArgumentInvalidTypeError(
                        f"Unsupported feature argument type: {arg_type}. "
                        f"argument name: {argument_name}, "
                        f"feature: {feature_name}")

            # 3. Validate the options of the argument
            if argument_settings.get("options"):
                if arg_data:
                    if not isinstance(arg_data, (list, tuple)):
                        arg_iter = [arg_data]
                    else:
                        arg_iter = arg_data

                    for i in arg_iter:
                        if i not in argument_settings.get("options"):
                            raise FeatureArgumentUnsupportedValueError(
                                f"Unsupported feature argument value: {i}. "
                                f"argument name: {argument_name}, "
                                f"feature: {feature_name}")

            # Add the validated argument
            validated_args[argument_name] = feature_args[argument_name]

        # Map the validated feature arguments
        return validated_args
