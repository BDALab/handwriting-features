import os
from handwriting_features.features import HandwritingFeatures


# Prepare the path to example data
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")


# Prepare the subject group
subject_group = "HC-female"
# subject_group = "HC-male"
# subject_group = "PD-female"
# subject_group = "PD-male"

# Prepare the filename of the signal to be used
signal_name = "00026_w.cz.fnusa.1_1.svc"

# Prepare the handwriting variables
variables = ["y", "x", "time", "pen_status", "azimuth", "tilt", "pressure"]

# Prepare the sampling frequency
fs = 133


if __name__ == "__main__":

    # Instantiate the handwriting features object from an example signal
    feature_sample = HandwritingFeatures.from_svc(os.path.join(data_path, subject_group, signal_name), variables)

    # Compute the handwriting features
    #
    # 1. Kinematic features
    #    a) velocity
    #    b) acceleration
    #    c) jerk
    # 2. Dynamic features
    #    a) azimuth
    #    b) tilt
    #    c) pressure
    # 3. Spatial features
    #    a) stroke length
    #    b) stroke height
    #    c) stroke width
    #    d) writing length
    #    e) writing height
    #    f) writing width
    # 4. Temporal features
    #    a) stroke duration
    #    b) ratio of stroke durations (on-surface / in-air strokes)
    #    c) writing duration
    #    d) writing duration overall
    #    e) ratio of writing durations (on-surface / in-air writing)
    #    f) number of interruptions
    #    g) number of interruptions_relative
    # 5. Composite features
    #    a) writing tempo
    #    b) writing stops
    #    c) writing number of changes

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

    # 5. Composite features
    feature_sample.writing_tempo(in_air=False)
    feature_sample.writing_stops(statistics=["mean", "std"])
    feature_sample.writing_number_of_changes(in_air=True, fs=fs)
