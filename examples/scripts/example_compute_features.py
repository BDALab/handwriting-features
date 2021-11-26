import os
from handwriting_features.features import HandwritingFeatures


# Prepare the path to example data
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")


if __name__ == "__main__":

    # Instantiate the handwriting features object from an example signal
    feature_sample = HandwritingFeatures.from_json(path=os.path.join(data_path, "signal.json"))

    # Compute the handwriting features
    #
    # 1. Kinematic features
    # 2. Dynamic features
    # 3. Spatial features
    # 4. Temporal features

    # 1. Kinematic features
    feature_sample.velocity(axis="x", in_air=False, statistics=["mean", "std"])
    feature_sample.acceleration(axis="y", in_air=True, statistics=["median", "iqr"])
    feature_sample.jerk(axis="xy", in_air=False)

    # 2. Dynamic features
    feature_sample.azimuth(in_air=False, statistics=["cv_parametric"])
    feature_sample.tilt(in_air=True, statistics=["cv_nonparametric"])
    feature_sample.pressure(statistics=())

    # 3. Spatial features
    feature_sample.stroke_length(in_air=False, statistics=["quartile_1", "quartile_3"])
    feature_sample.stroke_height(in_air=True, statistics=["slope_of_linear_regression"])
    feature_sample.stroke_width(in_air=False, statistics=())

    # 4. Temporal features
    feature_sample.stroke_duration(in_air=False, statistics=["percentile_5", "percentile_95"])
    feature_sample.ratio_of_stroke_durations(statistics=())
    feature_sample.writing_duration(in_air=True)
    feature_sample.ratio_of_writing_durations()
