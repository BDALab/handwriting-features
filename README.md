# Handwriting features

![GitHub last commit](https://img.shields.io/github/last-commit/BDALab/handwriting-features)
![GitHub issues](https://img.shields.io/github/issues/BDALab/handwriting-features)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BDALab/handwriting-features)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/handwriting-features)
![GitHub top language](https://img.shields.io/github/languages/top/BDALab/handwriting-features)
![PyPI - License](https://img.shields.io/pypi/l/handwriting-features)

This package provides an easy-to-use modern library for the extraction of a variety of common handwriting features focused on the domain of kinematic, dynamic, spatial, and temporal analysis of online handwriting/drawing. It is built on top of the [Handwriting sample](https://github.com/BDALab/handwriting-sample/) package for easy class-based manipulation with online handwriting data.

It also provides an interface for the Featurizer API: 
1. [Server side](https://github.com/BDALab/featurizer-api/) (RESTful API for feature extraction via injected features extraction library)
2. [Client side](https://github.com/BDALab/featurizer-api-client/) (lightweight client application)

_The full programming sphinx-generated docs can be seen in `docs/`_.

**Contents**:
1. [Installation](#Installation)
2. [Features](#Features)
3. [Usage](#Usage)
4. [Interface](#Interface)
5. [Examples](#Examples)
6. [License](#License)
7. [Contributors](#Contributors)

---

## Installation

```
pip install handwriting-features
```

## Features

The following list of handwriting features is supported:
1. kinematic features
   1. velocity
   2. acceleration
   3. jerk
2. dynamic features
   1. azimuth
   2. tilt
   3. pressure
3. spatial features
   1. stroke length
   2. stroke height
   3. stroke width
4. temporal features
   1. stroke duration
   2. ratio of stroke durations (on-surface / in-air strokes)
   3. writing duration
   4. ratio of writing durations (on-surface / in-air writing)

## Usage

The main entry point and the class to be used for the computation of the handwriting features is named `HandwritingFeatures`. To compute the features, an instance of `HandwritingFeatures` must be created using valid handwriting data in the form of an instance of the wrapper on top of the `HadwritingSample` named `HandwritingSampleWrapper`. The `HandwritingSample` is a class for the manipulation with online handwriting data installed from [this repository](https://github.com/BDALab/handwriting-sample/). The `HandwritingSampleWrapper` is used to enrich the `HandwritingSample` with the capabilities specific to the feature extraction.

To support alternative ways of instantiating the `HandwritingFeatures` from handwriting data stored in various data/file formats, the `HandwritingFeatures` provides the following alternative constructor methods:
1. for various data formats
   1. `from_list`
   2. `from_numpy_array`
   3. `from_pandas_dataframe`
2. for various file formats
   1. `from_json`
   2. `from_svc`

After the `HandwritingFeatures` object is instantiated, the supported handwriting features can be computed using the following methods:
1. kinematic features
   1. `velocity`
   2. `acceleration`
   3. `jerk`
2. dynamic features
   1. `azimuth`
   2. `tilt`
   3. `pressure`
3. spatial features
   1. `stroke_length`
   2. `stroke_height`
   3. `stroke_width`
4. temporal features
   1. `stroke_duration`
   2. `ratio_of_stroke_durations`
   3. `writing_duration`
   4. `ratio_of_writing_durations`

For more information, see the [Examples](#Examples) section.

## Interface

Besides the convenient use of the `HandwritingFeatures` interface class, the library also provides an interface for the [Featurizer API](https://github.com/BDALab/featurizer-api/) at `src/handwriting_features/interface/featurizer/`. The Featurizer API supports the feature extraction from handwriting data of 1-M subjects given the pipeline of features. This offers an additional option to extract a variety of handwriting features via a micro-service type of architecture via injecting the handwriting features library into the API as the feature extractor to be used. For more information, see the [official documentation](https://featurizer-api.readthedocs.io/en/latest/) of the Featurizer API.

## Examples

For more information about the example data, see the info file at `examples/data/info.json`.

### 1. compute handwriting features

```python
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


# Instantiate the handwriting features object from an example signal
feature_path = str(os.path.join(data_path, subject_group, signal_name))
feature_data = HandwritingFeatures.from_svc(feature_path, variables)

# Handwriting features:
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
# 4. Temporal features
#    a) stroke duration
#    b) ratio of stroke durations (on-surface / in-air strokes)
#    c) writing duration
#    d) ratio of writing durations (on-surface / in-air writing)

# 1. Kinematic features
feature_data.velocity(axis="x", in_air=False, statistics=["mean", "std"])
feature_data.acceleration(axis="y", in_air=True, statistics=["median", "iqr"])
feature_data.jerk(axis="xy", in_air=False)

# 2. Dynamic features
feature_data.azimuth(in_air=False, statistics=["cv_parametric"])
feature_data.tilt(in_air=True, statistics=["cv_nonparametric"])
feature_data.pressure(statistics=())

# 3. Spatial features
feature_data.stroke_length(in_air=False, statistics=["quartile_1", "quartile_3"])
feature_data.stroke_height(in_air=True, statistics=["slope_of_linear_regression"])
feature_data.stroke_width(in_air=False, statistics=())

# 4. Temporal features
feature_data.stroke_duration(in_air=False, statistics=["percentile_5", "percentile_95"])
feature_data.ratio_of_stroke_durations(statistics=())
feature_data.writing_duration(in_air=True)
feature_data.ratio_of_writing_durations()
```

### 2. plot handwriting features

```python
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

# Instantiate the handwriting features object from an example signal
feature_path = str(os.path.join(data_path, subject_group, signal_name))
feature_data = HandwritingFeatures.from_svc(feature_path, variables)

# Extract the loaded data
loaded_data = feature_data.sample

# Handwriting features:
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
# 4. Temporal features
#    a) stroke duration
#    b) ratio of stroke durations (on-surface / in-air strokes)
#    c) writing duration
#    d) ratio of writing durations (on-surface / in-air writing)

# Prepare the features computation
axis = "x"
in_air = False
statistics = ()

# 1. Compute the kinematic features
feature = feature_data.velocity(axis=axis, in_air=in_air, statistics=statistics)
# feature = feature_data.acceleration(axis=axis, in_air=in_air, statistics=statistics)
# feature = feature_data.jerk(axis=axis, in_air=in_air, statistics=statistics)

# 2. Compute the dynamic features
# feature = feature_data.azimuth(in_air=in_air, statistics=statistics)
# feature = feature_data.tilt(in_air=in_air, statistics=statistics)
# feature = feature_data.pressure(statistics=statistics)

# 3. Compute the spatial features
# feature = feature_data.stroke_length(in_air=in_air, statistics=statistics)
# feature = feature_data.stroke_height(in_air=in_air, statistics=statistics)
# feature = feature_data.stroke_width(in_air=in_air, statistics=statistics)

# 4. Compute the temporal features
# feature = feature_data.stroke_duration(in_air=in_air, statistics=statistics)
# feature = feature_data.ratio_of_stroke_durations(statistics=statistics)
# feature = feature_data.writing_duration(in_air=in_air)
# feature = feature_data.ratio_of_writing_durations()

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
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This package is developed by the members of [Brain Diseases Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact the head of the laboratory Jiri Mekyska <mekyska@vut.cz> or the main developer: Zoltan Galaz <galaz@vut.cz>.