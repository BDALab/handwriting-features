from handwriting_features.interface.featurizer.handlers import MultiSubjectFeatureExtractorHandler


class FeatureExtractor(object):
    """
    Class implementing the features extractor interface for the Featurizer API.

    For more information about featurizer, see the following repositories:
    1. [server side](#github.com/BDALab/featurizer-api)
    1. [client side](#github.com/BDALab/featurizer-api-client)

    For more information about the attributes, see: ``extract(...)``
    """

    def __init__(self, values, labels=None, **configuration):
        """
        Initializes the FeatureExtractor featurizer API interface.

        :param values: data values to extract the features from
        :type values: numpy.ndarray
        :param labels: data labels for data samples, defaults to None
        :type labels: list, optional
        :param configuration: common extractor configuration
        :type configuration: **kwargs, optional
        """

        # Set the sample values/labels
        self.values = values
        self.labels = labels if labels else []

        # Set the extractor configuration
        self.configuration = configuration if configuration else {}

        # Initialize the handler
        self.handler = MultiSubjectFeatureExtractorHandler

    def extract(self, pipeline):
        """
        Interface method: extract the features.

        **Data**

        1. data is of type: ``numpy.ndarray``.
        2. data is mandatory.
        3. data shape: In general, data to have the shape (M, ..., D). Where M
           stands for subjects (i.e. subjects are in the first dimension), and
           D stands for D data samples (of shape ...).
            1. in the case of data having the following shape: (D, ), the API
               assumes it is a vector of D data sample points for one subject.
               It transforms the data to a row vector: (1, D) to add the
               dimension for the subject.
            2: in the case of data having the following shape: (M, ..., D),
               the API does not transform the data, but it assumes there are
               M subjects abd D data samples, each having (...) dimensionality,
               e.g. if data has the shape (M, 3, 10) it means that there are
               M subjects and each of the subjects has 10 data samples (each
               being three dimensional).

        **Labels**

        1. labels are of type: ``list``.
        2. labels are optional.
        3. labels are of length D (for each data sample, there is one label)

        **Configuration**

        1. configuration are of type: ``dict``.
        2. configuration is optional.
        3. configuration provides common kwargs for feature extraction

        **Pipeline**

        1. pipeline is of type: ``list``.
        2. pipeline is mandatory.
        3. each element in the pipeline is of type: ``dict``.
        4. each element in the pipeline has the following keys: a) ``name``
           to hold the name of the feature to be computed, and b) ``args``
           to hold the arguments (kwargs) for the specific feature extraction
           method that is going to be used (it is of type: ``dict``).

        **Output**

        The extracted features follow the same shape convention as the input
        data: the subjects are in the first dimension, and the features are
        in the last dimension (each feature having shape ...).

        :param pipeline: pipeline of the features to be extracted
        :type pipeline: list
        :return: extracted features and labels
        :rtype: dict {"features": ..., "labels": ...}
        """
        return self.handler.extract(self.values, self.labels, pipeline, **self.configuration)
