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

```python
from handwriting_features.features import HandwritingFeatures

# Instantiate the handwriting features object
feature_sample = HandwritingFeatures.from_svc(path="path_to_file")

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
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This package is developed by the members of [Brain Diseases Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact the head of the laboratory Jiri Mekyska <mekyska@vut.cz> or the main developer: Zoltan Galaz <galaz@vut.cz>.