import os
import matplotlib.pyplot as plt
from pprint import pprint
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


if __name__ == "__main__":

    # Temporal features:
    #
    # 1. stroke_duration
    # 2. ratio_of_stroke_durations
    # 3. writing_duration
    # 4. ratio_of_writing_durations

    # Instantiate the handwriting features object from an example signal
    feature_sample = HandwritingFeatures.from_svc(os.path.join(data_path, subject_group, signal_name), variables)

    # Extract the loaded data
    loaded_data = feature_sample.sample

    # Prepare the features computation
    in_air = False
    statistics = ()

    # Compute the temporal features
    feature = feature_sample.stroke_duration(in_air=in_air, statistics=statistics)
    # feature = feature_sample.ratio_of_stroke_durations(statistics=statistics)
    # feature = feature_sample.writing_duration(in_air=in_air)
    # feature = feature_sample.ratio_of_writing_durations()

    pprint(feature)

    # Plot the original data and the computed feature
    if not statistics:

        fig = plt.figure(figsize=(16, 10))

        # Plot the original data
        ax = fig.add_subplot(1, 2, 1)
        ax.plot(loaded_data.sample_x, loaded_data.sample_y, "-", color="blue", linewidth=2, alpha=0.7)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)

        # Plot the original data
        ax = fig.add_subplot(1, 2, 2)
        ax.plot(feature, "-", color="red", linewidth=2, alpha=0.7)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)

        # Adjust the figure
        fig.tight_layout()

        # Store the graphs
        # plt.savefig(f"{signal_name}.pdf", bbox_inches="tight")

        # Show the graphs
        plt.get_current_fig_manager().window.state("zoomed")
        plt.show()
