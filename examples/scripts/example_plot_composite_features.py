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

    # Composite features:
    #
    # 1. writing tempo
    # 2. writing stops
    # 3. number of changes in x profile
    # 4. number of changes in y profile
    # 5. number of changes in azimuth
    # 6. number of changes in tilt
    # 7. number of changes in pressure
    # 8. number of changes in velocity profile
    # 9. relative number of changes in x profile
    # 10. relative number of changes in y profile
    # 11. relative number of changes in azimuth
    # 12. relative number of changes in tilt
    # 13. relative number of changes in pressure
    # 14. relative number of changes in velocity profile

    # Instantiate the handwriting features object from an example signal
    feature_sample = HandwritingFeatures.from_svc(os.path.join(data_path, subject_group, signal_name), variables)

    # Extract the loaded data (wrapped handwriting sample)
    loaded_data = feature_sample.wrapper

    # Prepare the features computation
    in_air = False
    statistics = ()

    # Prepare the sampling frequency
    fs = 133

    # Compute the composite features
    feature = feature_sample.writing_tempo(in_air=in_air)
    # feature = feature_sample.writing_stops(statistics=statistics)
    # ...

    pprint(feature)

    # Plot the original data and the computed feature
    if not statistics:

        fig = plt.figure(figsize=(16, 10))

        # Plot the original data
        ax = fig.add_subplot(1, 2, 1)
        ax.plot(loaded_data.sample_x, loaded_data.sample_y, "-", color="blue", linewidth=2, alpha=0.7)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)

        # Plot the feature
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
