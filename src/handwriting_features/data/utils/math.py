import numpy
import pandas


def derivation(array, order=1):
    """
    Returns a derivation of input <array>.

    :param array: input array
    :type array: numpy.ndarray
    :param order: order of derivation, defaults to 1
    :type order: int, optional
    :return: derivation
    :rtype: numpy.ndarray
    """
    return numpy.diff(array, order, axis=0) if isinstance(array, numpy.ndarray) else numpy.nan


def intersection(x1, y1, x2=None, y2=None):
    """
    Computes the intersection of two curves.
    Inspired by: https://www.mathworks.com/matlabcentral/fileexchange/22441-curve-intersections

    :param x1: x-values of the first curve
    :type x1: numpy.ndarray
    :param y1: y-values of the first curve
    :type y1: numpy.ndarray
    :param x2: x-values of the second curve
    :type x2: numpy.ndarray
    :param y2: y-values of the second curve
    :type y2: numpy.ndarray
    :return: intersections
    :rtype: numpy.ndarray
    """

    # Prepare the input variables
    x1 = pandas.DataFrame(x1) if not isinstance(x1, pandas.DataFrame) else x1
    y1 = pandas.DataFrame(y1) if not isinstance(y1, pandas.DataFrame) else y1
    x2 = pandas.DataFrame(x2) if (x2 is not None and not isinstance(x2, pandas.DataFrame)) else x2
    y2 = pandas.DataFrame(y2) if (y2 is not None and not isinstance(y2, pandas.DataFrame)) else y2

    # Prepare the handling of the intersections (based on the presence of the second curve)
    #
    # 1. if the second curve is not provided, shared points will not be returned
    # 2. if the second curve is provided, all intersection points will be returned
    second_curve_exists = False if x2 is None else True

    # Handle the presence of the second curve
    if not second_curve_exists:
        x2 = x1
        y2 = y1
        x2 = numpy.mat(x2.values).transpose()
        y2 = numpy.mat(y2.values).transpose()
    else:
        x2 = numpy.mat(x2.values).transpose()
        y2 = numpy.mat(y2.values).transpose()

    # Convert the 1st curve to column-vectors
    x1 = numpy.mat(x1.values)
    y1 = numpy.mat(y1.values)

    # Combine x and y for each curve to one master matrix
    #
    # 1. the 1st curve - column vector
    # 2. the 2nd curve - row vector
    curve1 = numpy.hstack([x1, y1])
    curve2 = numpy.vstack([x2, y2])

    x1 = curve1.transpose()[0].transpose()
    y1 = curve1.transpose()[1].transpose()
    x2 = curve2[0]
    y2 = curve2[1]

    # Compute the distance between adjacent x's and y's
    dx1 = numpy.diff(x1, axis=0)
    dx2 = numpy.diff(x2)
    dy1 = numpy.diff(y1, axis=0)
    dy2 = numpy.diff(y2)

    # Compute the signed differences
    s1 = numpy.multiply(dx1, y1[0:len(y1) - 1]) - numpy.multiply(dy1, x1[0:len(x1) - 1])
    s2 = \
        numpy.multiply(dx2, y2.transpose()[0:len(y2.transpose()) - 1].transpose()) - \
        numpy.multiply(dy2, x2.transpose()[0:len(x2.transpose()) - 1].transpose())

    f1 = dx1 * y2 - dy1 * x2
    f2 = y1 * dx2 - x1 * dy2

    f2t = f2.transpose()
    s2t = s2.transpose()

    # Collected distances between points in one curve and line segments in the other
    c1 = numpy.multiply(
        f1[0:int(f1.shape[0]), 0:int(f1.shape[1]) - 1] - s1,
        f1[0:int(f1.shape[0]), 1:int(f1.shape[1])] - s1)
    c2 = numpy.multiply(
        f2t[0:int(f2t.shape[0]), 0:int(f2t.shape[1]) - 1] - s2t,
        f2t[0:int(f2t.shape[0]), 1:int(f2t.shape[1])] - s2t)

    # If looking for self-intersections, take only points that aren't tangential
    if not second_curve_exists:
        tf1 = c1 < 0
        tf2 = c2 < 0

    # Otherwise, take tangent points as well
    else:
        tf1 = c1 <= 0
        tf2 = c2 <= 0

    tf2 = tf2.transpose()

    # Keep indicates row and column indices of line segments where intersections between the two curves are expected
    keep = tf1 & tf2

    # Collect row and column index values from the keep matrix
    i = []
    j = []
    for row in range(keep.shape[0]):
        for column in range(keep.shape[1]):
            if keep[row, column]:
                i.append(row)
                j.append(column)

    if not i:
        return pandas.DataFrame({"xs": [None], "xy": [None]}, columns=["xs", "ys"])

    # Transpose the distances
    dy2 = dy2.transpose()
    dx2 = dx2.transpose()

    # Prepare the computation
    r = numpy.multiply(dy2[j], dx1[i]) - numpy.multiply(dy1[i], dx2[j])

    r_prime = []
    i_prime = []
    j_prime = []

    for num in range(r.shape[0]):
        if r[num] != 0:
            r_prime.append(r[num, 0])
            i_prime.append(i[num])
            j_prime.append(j[num])

    r_prime = numpy.mat(r_prime).transpose()

    # Set up numerator and denominator to solve the system of equations
    numerator = numpy.hstack([
        numpy.multiply(dx2[j_prime], s1[i_prime]) - numpy.multiply(dx1[i_prime], s2t[j_prime]),
        numpy.multiply(dy2[j_prime], s1[i_prime]) - numpy.multiply(dy1[i_prime], s2t[j_prime])
    ])
    denominator = numpy.hstack([
        r_prime,
        r_prime
    ])

    # Solve the system of equations
    result = numpy.divide(numerator, denominator)

    # Organize the intersections into pandas DataFrame
    intersections = pandas.DataFrame(result, columns=["xs", "ys"])
    intersections = intersections.drop_duplicates(inplace=False)

    # Return the intersections
    return intersections.values
