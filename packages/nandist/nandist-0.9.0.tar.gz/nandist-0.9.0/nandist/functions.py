"""NA-ignoring distance functions for calculating the distance between two arrays"""

from functools import wraps
import numpy as np
import scipy


def zero_self_distance(f):
    """Ensure self distance is zero"""

    @wraps(f)
    def inner(u, v, **kwargs):
        if np.array_equal(u, v):
            return 0
        else:
            return f(u, v, **kwargs)

    return inner


def ignore_na_minkowski(*args, **kwargs):
    """NA-ignoring minkowski distance"""

    @wraps(scipy.spatial.distance.minkowski)
    def inner(u, v, p=2, w=None):
        """"""
        u0, v0 = np.nan_to_num(u), np.nan_to_num(v)

        # Correction expects a weights vector to be present
        if w is None:
            w = np.ones_like(u)

        # Numpy takes a different route for cityblock than other minkowski-like distances where p != 1
        # This ensures we take the same route
        if p == 1:
            y = scipy.spatial.distance.cityblock(u0, v0, w=w)
        else:
            y = scipy.spatial.distance.minkowski(u0, v0, p=p, w=w)

        # Correction
        u_delta = np.dot(np.isnan(u), w * v0)
        v_delta = np.dot(w * u0, np.isnan(v))

        # Return early answer if corrects add up to zero
        if (correction := u_delta + v_delta) < np.finfo("float").eps:
            return y

        return (y**p - correction) ** (1 / p)

    return inner


def ignore_na_chebyshev(*args, **kwargs):
    """NA-ignoring Chebyshev distance"""

    @wraps(scipy.spatial.distance.chebyshev)
    def inner(u, v, **kwargs):

        # Replace u_i, v_i with zero if u_i is NA or if v_i is NA
        # No correction on distance calculated with zero-imputed arrays necessary.
        nan = np.isnan(u) | np.isnan(v)
        u0, v0 = u, v
        u[nan] = 0
        v[nan] = 0

        return scipy.spatial.distance.chebyshev(u0, v0, **kwargs)

    return inner


def ignore_na_cosine(*args, **kwargs):
    """NA-ignoring cosine distance"""

    @wraps(scipy.spatial.distance.cosine)
    def inner(u, v, **kwargs):
        # Replace u_i, v_i with zero if u_i is NA or if v_i is NA
        # No correction on distance calculated with zero-imputed arrays necessary.
        nan = np.isnan(u) | np.isnan(v)
        u0, v0 = u, v
        u[nan] = 0
        v[nan] = 0
        return scipy.spatial.distance.cosine(u0, v0, **kwargs)

    return inner


def ignore_na_euclidean(*args, **kwargs):
    """NA-ignoring euclidean distance"""

    @wraps(scipy.spatial.distance.euclidean)
    def inner(u, v, w=None):
        return minkowski(u, v, p=2, w=w)

    return inner


def ignore_na_cityblock(*args, **kwargs):
    """NA-ignoring cityblock distance"""

    @wraps(scipy.spatial.distance.cityblock)
    def inner(u, v, w=None):
        return minkowski(u, v, p=1, w=w)

    return inner


@zero_self_distance
@ignore_na_euclidean
def euclidean(*args, **kwargs):
    return


@zero_self_distance
@ignore_na_minkowski
def minkowski(*args, **kwargs):
    return


@zero_self_distance
@ignore_na_cityblock
def cityblock(*args, **kwargs):
    return


@zero_self_distance
@ignore_na_chebyshev
def chebyshev(*args, **kwargs):
    return


@zero_self_distance
@ignore_na_cosine
def cosine(*args, **kwargs):
    return
