from hypothesis.extra.numpy import arrays, from_dtype
from hypothesis.strategies import integers, composite
import numpy as np

# Test array of floats without infinities but with nans (allowed, not required)
test_array = arrays(
    np.dtype("float"),
    shape=(1, 5),
    elements=from_dtype(np.dtype("float"), allow_nan=True, allow_infinity=False),
)

# Array lengths
MIN_LENGTH = 1
MAX_LENGTH = 1_000


@composite
def normal_arrays(draw, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
    """Hypothesis strategy for returning a matrix with shape = (3, length), with random length between min_length and
    max_length"""
    length = draw(integers(min_value=min_length, max_value=max_length))

    # Draw random array, ensure that the sum of elements is less than the max float to prevent testing errors
    return draw(
        arrays(
            np.dtype("float"),
            shape=(3, length),
            elements=from_dtype(
                np.dtype("float"), allow_nan=False, allow_infinity=False
            ),
        ).filter(lambda x: np.sum(x) < np.finfo("float").max)
    )


@composite
def nan_zero_arrays(draw, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
    """Return a (2, length) sized matrix containing only zeros or NaNs"""
    length = draw(integers(min_value=min_length, max_value=max_length))
    return draw(
        arrays(
            np.dtype("float"),
            shape=(2, length),
            elements=from_dtype(
                np.dtype("float"),
                allow_nan=True,
                allow_infinity=False,
                min_value=0,
                max_value=0,
            ),
        )
    )


@composite
def nan_arrays(draw, min_length=MIN_LENGTH, max_length=MAX_LENGTH):
    """Hypothesis strategy for returning a matrix with shape = (3, length), with random length between min_length and
    max_length. The matrix consists of vectors a, b, and w.
    The filter ensures that either a or b contains at least one NAN value"""
    length = draw(integers(min_value=min_length, max_value=max_length))

    # Draw random array, filter such that:
    # 1: there is at least one NaN in the first two arrays
    # 2: the sum of all elements is smaller than the maximum float

    # The reason for (2) is that we will be testing whether the nandist calculated distance is equal to the scipy
    # distance alculated for an array where NaN elements are removed. In our implementation, we might overestimate the
    # distance and then correct for this overestimation. However, the overestimation can lead to infinite values.
    # To prevent these infinities, the sum of elements of each vector cannot exceed the maximum float value.
    return draw(
        arrays(
            np.dtype("float"),
            shape=(3, length),
            elements=from_dtype(
                np.dtype("float"), allow_nan=True, allow_infinity=False
            ),
        )
        .filter(lambda x: np.any(np.isnan(x[:2])))  # filter (1)
        .filter(
            lambda x: np.all(np.sum(np.nan_to_num(x, 0), 1) < np.finfo("float").max)
        )  # filter (2)
    )
