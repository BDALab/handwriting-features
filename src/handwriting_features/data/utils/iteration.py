from itertools import islice
from collections import deque


def sliding_window(iterable, size, step, padding=None):
    """
    Apply sliding_window on an input iterable given the windowing arguments.

    :param iterable: iterable to be iterated over
    :type iterable: iterable
    :param size: window size
    :type size: int
    :param step: window step
    :type step: int
    :param padding: window padding, defaults to None
    :type padding: Any, optional
    :return: windowed iterable
    :rtype: iterator
    """

    # Prepare the queue
    i = iter(iterable)
    q = deque(islice(i, size), maxlen=size)
    if not q:
        return

    # Apply the window
    q.extend(padding for _ in range(size - len(q)))
    while True:
        yield iter(q)
        try:
            q.append(next(i))
        except StopIteration:
            return
        q.extend(next(i, padding) for _ in range(step - 1))
