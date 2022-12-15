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

    # Spatial features:
    #
    # 1. stroke_length
    # 2. stroke_height
    # 3. stroke_width
    # 4. writing length
    # 5. writing height
    # 6. writing width
    # 7. number of intra-stroke intersections
    # 8. relative number of intra-stroke intersections
    # 9. total number of intra-stroke intersections
    # 10. relative total number of intra-stroke intersections
    # 11. number of inter-stroke intersections
    # 12. relative number of inter-stroke intersections
    # 13. vertical peaks indices
    # 14. vertical valleys indices
    # 15. vertical peaks values
    # 16. vertical valleys values
    # 17. vertical peaks velocity
    # 18. vertical valleys velocity
    # 19. vertical peaks distance
    # 20. vertical valleys distance
    # 21. vertical peaks duration
    # 22. vertical valleys duration

    # Instantiate the handwriting features object from an example signal
    feature_sample = HandwritingFeatures.from_svc(os.path.join(data_path, subject_group, signal_name), variables)

    # Extract the loaded data (wrapped handwriting sample)
    loaded_data = feature_sample.wrapper

    # Prepare the features computation
    in_air = False
    statistics = ()

    # Compute the spatial features
    feature = feature_sample.stroke_length(in_air=in_air, statistics=statistics)
    # feature = feature_sample.stroke_height(in_air=in_air, statistics=statistics)
    # feature = feature_sample.stroke_width(in_air=in_air, statistics=statistics)

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
