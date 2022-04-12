import numpy


def get_stroke_indexes(strokes):
    """Gets the indexes of the strokes"""

    # Prepare the list of indexes
    indexes = []

    # Get the indexes
    for i in range(len(strokes)):
        if i == 0:
            indexes.append(0)
        else:
            indexes.append(indexes[i - 1] + len(strokes[i - 1].time))

    # Return the indexes
    return indexes


def get_borders(array, border_value=0):
    """Gets borders of an array given a border value"""

    # Get the shifted arrays
    array_l = array[:-1]
    array_r = array[1:]

    # Get the borders
    border_l = numpy.where(numpy.logical_and(array_r == border_value, array_l != border_value))[0]
    border_r = numpy.where(numpy.logical_and(array_r != border_value, array_l == border_value))[0]

    if array[0] == border_value:
        border_l = numpy.array([0] + border_l.tolist())
    if array[-1] == border_value:
        border_r = numpy.array(border_r.tolist() + [len(array)])

    # Return the borders
    return border_l, border_r


def fuze_pauses(border_left, border_right, num_samples):
    """Fuze the pauses"""

    # Fuze the pauses
    if len(border_left) > 1:
        for i in range(len(border_left) - 1):
            if border_left[i + 1] - border_right[i] < (2 * num_samples):
                border_left[i + 1], border_right[i] = numpy.nan, numpy.nan

        # Remove improper pauses
        remove = [i for i, (l, r) in enumerate(zip(border_left, border_right)) if numpy.isnan(l) and numpy.isnan(r)]
        border_left = numpy.delete(border_left, remove)
        border_right = numpy.delete(border_right, remove)

        nans_right = numpy.isnan(border_right)
        if nans_right.any():

            border_right = numpy.array([
                border_right[i + 1] if is_nan else border_right[i]
                for i, is_nan in zip(range(len(border_right)), nans_right)
            ])

            border_left = numpy.delete(border_left, numpy.where(nans_right)[0] + 1)
            border_right = numpy.delete(border_right, numpy.where(nans_right)[0] + 1)

    # Return the fused pauses
    return border_left, border_right
