import numpy
import warnings
from handwriting_features.data.utils.cleanup import remove_outliers
from handwriting_features.data.exceptions.statistics import *


# Ignore numpy warnings
warnings.filterwarnings("ignore")


def mean(array):
    """
    Computes mean of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: mean value
    :rtype: numpy.float
    """
    return numpy.nanmean(array) if numpy.isfinite(array).any() else numpy.nan


def std(array):
    """
    Computes std of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: std value
    :rtype: numpy.float
    """
    return numpy.nanstd(array) if numpy.isfinite(array).any() else numpy.nan


def cv_parametric(array, as_percentage=False):
    """
    Computes parametric cv of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :param as_percentage: percentage computation flag, defaults to False
    :type as_percentage: bool, optional
    :return: parametric cv value
    :rtype: numpy.float
    """

    # Get the mean and standard deviation
    _avg = mean(array)
    _std = std(array)

    # Compute the parametric cv
    if any((not numpy.isfinite(_avg), not numpy.isfinite(_std))):
        return numpy.nan
    else:
        return (_std / (_avg + numpy.finfo(float).eps)) * (1 if not as_percentage else 100)


def median(array):
    """
    Computes median of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: median value
    :rtype: numpy.float
    """
    return numpy.nanmedian(array) if numpy.isfinite(array).any() else numpy.nan


def iqr(array):
    """
    Computes iqr of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: iqr value
    :rtype: numpy.float
    """

    # Get the quartiles
    _q1 = numpy.nanquantile(array, 0.25)
    _q3 = numpy.nanquantile(array, 0.75)

    # Compute the iqr
    if any((not numpy.isfinite(_q1), not numpy.isfinite(_q3))):
        return numpy.nan
    else:
        return numpy.subtract(_q3, _q1)


def cv_nonparametric(array, as_percentage=False):
    """
    Computes non-parametric cv of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :param as_percentage: percentage computation flag, defaults to False
    :type as_percentage: bool, optional
    :return: non-parametric cv value
    :rtype: numpy.float
    """

    # Get the iqr and median
    _med = median(array)
    _iqr = iqr(array)

    # Compute the non-parametric cv
    if any((not numpy.isfinite(_med), not numpy.isfinite(_iqr))):
        return numpy.nan
    else:
        return (_iqr / _med + numpy.finfo(float).eps) * (1 if not as_percentage else 100)


def quartile_1(array):
    """
    Computes 1st quartile of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: 1st quartile value
    :rtype: numpy.float
    """
    return numpy.nanquantile(array, 0.25) if numpy.isfinite(array).any() else numpy.nan


def quartile_3(array):
    """
    Computes 3rd quartile of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: 3rd quartile value
    :rtype: numpy.float
    """
    return numpy.nanquantile(array, 0.75) if numpy.isfinite(array).any() else numpy.nan


def percentile_5(array):
    """
    Computes 5th percentile of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: 5th percentile value
    :rtype: numpy.float
    """
    return numpy.nanpercentile(array, 5) if numpy.isfinite(array).any() else numpy.nan


def percentile_95(array):
    """
    Computes 95th percentile of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :return: 95th percentile value
    :rtype: numpy.float
    """
    return numpy.nanpercentile(array, 95) if numpy.isfinite(array).any() else numpy.nan


def slope_of_linear_regression(array, window_size=5, min_samples=3, center=True, threshold=3):
    """
    Computes slope of linear regression of an input array (ignoring NaNs).

    :param array: input array
    :type array: numpy.ndarray
    :param window_size: size of the moving window, defaults to 5
    :type window_size: int, optional
    :param min_samples: minimum number of samples in a window, defaults to 3
    :type min_samples: int, optional
    :param center: labels at the center of the window flag, defaults to True
    :type center: bool, optional
    :param threshold: outlier removal threshold, defaults to 3
    :type threshold: int, optional
    :return: slope of linear regression value
    :rtype: numpy.float
    """

    # Handle NaN/Inf value only
    if not isinstance(array, numpy.ndarray) and not numpy.isfinite(array):
        return numpy.nan

    # Create a local deepcopy of the input array
    data = numpy.copy(array)

    # Remove NaN/Inf values and flatten the array
    data = data[numpy.isfinite(data)]
    data = data.flatten("F")

    # Remove outliers
    if data.size > window_size:
        data = remove_outliers(data, window_size, min_samples=min_samples, center=center, threshold=threshold)

    # Handle empty array
    if data.size == 0:
        return numpy.nan

    # Fit the 1st order regression curve
    try:
        fitted = numpy.polyfit(list(range(len(data))), data, 1)
    except numpy.linalg.LinAlgError:
        return numpy.nan

    # Return the slope
    return fitted[0]


class Statistics(object):
    """Class implementing statistics computation interface"""

    # Mapping between statistics and computational functions
    mapping = {
        "mean": mean,
        "std": std,
        "cv_parametric": cv_parametric,
        "median": median,
        "iqr": iqr,
        "cv_nonparametric": cv_nonparametric,
        "quartile_1": quartile_1,
        "quartile_3": quartile_3,
        "percentile_5": percentile_5,
        "percentile_95": percentile_95,
        "slope_of_linear_regression": slope_of_linear_regression
    }

    @classmethod
    def compute(cls, array, statistical_function):
        """
        Computes the <statistical_function> of an input <array>.

        :param array: input array
        :type array: numpy.ndarray
        :param statistical_function: statistical function name
        :type statistical_function: str
        :return: computed statistics
        :rtype: numpy.float
        """

        # Validate input arguments
        if statistical_function not in cls.mapping:
            raise StatisticsNameNotInMappingError(f"Unsupported <statistical_function> {statistical_function}")
        if not isinstance(array, (float, numpy.ndarray)):
            raise UnsupportedDataForStatisticsError(
                f"Unsupported <array> type {type(array)}; "
                f"must be any of the following: `numpy.ndarray`, `numpy.float`")

        # Compute the statistical function
        return cls.mapping[statistical_function](array)
