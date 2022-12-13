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
            "velocity":
                self.features.velocity,
            "acceleration":
                self.features.acceleration,
            "jerk":
                self.features.jerk,

            # 2. Dynamic features
            "azimuth":
                self.features.azimuth,
            "tilt":
                self.features.tilt,
            "pressure":
                self.features.pressure,

            # 3. Spatial features
            "stroke_length":
                self.features.stroke_length,
            "stroke_height":
                self.features.stroke_height,
            "stroke_width":
                self.features.stroke_width,
            "writing_length":
                self.features.writing_length,
            "writing_height":
                self.features.writing_height,
            "writing_width":
                self.features.writing_width,
            "number_of_intra_stroke_intersections":
                self.features.number_of_intra_stroke_intersections,
            "relative_number_of_intra_stroke_intersections":
                self.features.relative_number_of_intra_stroke_intersections,
            "total_number_of_intra_stroke_intersections":
                self.features.total_number_of_intra_stroke_intersections,
            "relative_total_number_of_intra_stroke_intersections":
                self.features.relative_total_number_of_intra_stroke_intersections,
            "number_of_inter_stroke_intersections":
                self.features.number_of_inter_stroke_intersections,
            "relative_number_of_inter_stroke_intersections":
                self.features.relative_number_of_inter_stroke_intersections,

            # 4. Temporal features
            "stroke_duration":
                self.features.stroke_duration,
            "ratio_of_stroke_durations":
                self.features.ratio_of_stroke_durations,
            "writing_duration":
                self.features.writing_duration,
            "writing_duration_overall":
                self.features.writing_duration_overall,
            "ratio_of_writing_durations":
                self.features.ratio_of_writing_durations,
            "number_of_interruptions":
                self.features.number_of_interruptions,
            "number_of_interruptions_relative":
                self.features.number_of_interruptions_relative,

            # 5. Composite features
            "writing_tempo":
                self.features.writing_tempo,
            "writing_stops":
                self.features.writing_stops,
            "writing_number_of_changes":
                self.features.writing_number_of_changes
        }

        # Map the feature name to the feature computation method
        try:
            return mapping[feature_name]
        except KeyError:
            raise FeatureNameNotInMappingError(f"No mapping available for feature {feature_name}")
