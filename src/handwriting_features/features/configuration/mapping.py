from handwriting_features.features.exceptions.mapping import *


class HandwritingFeaturesMapping(object):
    """Class implementing the handwriting features mapping"""

    def __init__(self, features):
        """Constructor method"""
        self.features = features

    def map(self, feature_name):
        """Map the feature name to the actual feature computation method"""

        # Prepare the mapping (feature name: feature computation method)
        mapping = {

            # 1. Kinematic features
            "velocity": self.features.velocity,
            "acceleration": self.features.acceleration,
            "jerk": self.features.jerk,

            # 2. Dynamic features
            "azimuth": self.features.azimuth,
            "tilt": self.features.tilt,
            "pressure": self.features.pressure,

            # 3. Spatial features
            "stroke_length": self.features.stroke_length,
            "stroke_height": self.features.stroke_height,
            "stroke_width": self.features.stroke_width,

            # 4. Temporal features
            "stroke_duration": self.features.stroke_duration,
            "ratio_of_stroke_durations": self.features.ratio_of_stroke_durations,
            "writing_duration": self.features.writing_duration,
            "ratio_of_writing_durations": self.features.ratio_of_writing_durations
        }

        # Map the feature name to the feature computation method
        try:
            return mapping[feature_name]
        except KeyError:
            raise FeatureNameNotInMappingError(f"No mapping available for feature {feature_name}")
