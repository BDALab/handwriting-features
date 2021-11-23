import numpy
import pandas


def remove_outliers(array, window_size, min_samples=3, center=True, threshold=3, make_copy=False):
    """
    Removes outliers based on the rolling median.

    :param array: input array
    :type array: numpy.ndarray
    :param window_size: size of the moving window
    :type window_size: int
    :param min_samples: minimum number of samples in a window, defaults to 3
    :type min_samples: int, optional
    :param center: labels at the center of the window flag, defaults to True
    :type center: bool, optional
    :param threshold: outlier removal threshold, defaults to 3
    :type threshold: int, optional
    :param make_copy: copy creation flag, defaults to False
    :type make_copy: bool, optional
    :return: slope of linear regression value
    :rtype: numpy.float
    """

    # Make a local copy of an input array
    data = array.copy() if make_copy else array

    # Apply the rolling window calculation
    rolled = pandas.Series(data).rolling(window=window_size, min_periods=min_samples, center=center)

    # Filter out outliers
    filtered = [
        element for element, median in zip(array, rolled.median().values)
        if numpy.abs(element) < (threshold * numpy.abs(median))
    ]

    # Convert the filtered data into a numpy array
    filtered = numpy.array(filtered)

    # Remove NaN/Inf values and flatten the array
    filtered = filtered[numpy.isfinite(filtered)]
    filtered = filtered.flatten("F")

    # Return the filtered array
    return filtered
