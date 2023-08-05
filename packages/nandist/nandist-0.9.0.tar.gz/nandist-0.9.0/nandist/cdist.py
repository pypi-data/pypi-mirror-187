"""NA-ignoring replacement for scipy.spatial.distance.cdist"""

import scipy
import numpy as np
from functools import wraps


def ignore_na_cdist(*args, **kwargs):
    @wraps(scipy.spatial.distance.cdist)
    def inner(XA, XB, metric="euclidean", *, out=None, **kwargs):
        """The arguments are taken from the scipy API"""
        # No NANs present? Do nothing
        nans_in_A, nans_in_B = np.any(np.isnan(XA)), np.any(np.isnan(XB))
        if not nans_in_A and not nans_in_B:
            return scipy.spatial.distance.cdist(XA, XB, metric, out=out, **kwargs)

        if metric == "cityblock":
            return minkowski(XA, XB, out=out, p=1, **kwargs)
        elif metric == "euclidean":
            return minkowski(XA, XB, out=out, p=2, **kwargs)
        elif metric == "minkowski":
            return minkowski(XA, XB, out=out, **kwargs)
        elif metric == "cosine":
            return cosine(XA, XB, out=out, **kwargs)
        elif metric == "chebyshev":
            return chebyshev(XA, XB, out=out, **kwargs)
        else:
            raise NotImplementedError(
                f"NA-ignored distance {metric =} not implemented."
            )

    return inner


@ignore_na_cdist
def cdist(*args, **kwargs):
    return


def minkowski(XA, XB, **kwargs):
    """NA-ignoring Minkowski variant returning a square form distance matrix"""
    if np.all(np.isnan(XA) | np.isnan(XB)):
        return np.zeros(shape=(XA.shape[0], XA.shape[0]))

    p = kwargs.get("p", 2.0)  # get 'p' from kwargs, otherwise default to 2
    w = kwargs.get("w")
    out = kwargs.get("out")

    XA0 = np.nan_to_num(XA, nan=0)
    XB0 = np.nan_to_num(XB, nan=0)

    Dp = scipy.spatial.distance.cdist(XA0, XB0, "minkowski", out=out, w=w, p=p) ** p

    if w is None:
        w = np.ones_like(XA[0])

    Dp -= np.matmul(np.isnan(XA), (np.abs(w * XB0)).T) ** p
    Dp -= np.matmul(np.abs(w * XA0), np.isnan(XB).T) ** p

    return Dp ** (1 / p)


def cosine(XA, XB, **kwargs):
    """NA-ignoring cosine distance variant returning a square form distance matrix"""

    XA0 = np.nan_to_num(XA, nan=0)
    XB0 = np.nan_to_num(XB, nan=0)

    return scipy.spatial.distance.cdist(XA0, XB0, "cosine", **kwargs)


def chebyshev(XA, XB, **kwargs):
    """NA-ignoring chebyshev distance variant returning a square form distance matrix"""

    # Replace u_i, v_i with zero if u_i is NA or if v_i is NA
    nan = np.isnan(XA) | np.isnan(XB)
    XA0, XB0 = XA, XB
    XA[nan] = 0
    XB[nan] = 0

    return scipy.spatial.distance.cdist(XA0, XB0, "chebyshev", **kwargs)
