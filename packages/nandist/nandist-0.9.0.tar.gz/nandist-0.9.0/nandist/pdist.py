"""NA-ignoring replacement for scipy.spatial.distance.pdist
Calls cdist implementation and then converts to appropriate distance matrix form"""

import scipy
import numpy as np
from functools import wraps

from .cdist import minkowski, chebyshev, cosine


def convert_form(Y):
    """Return converted form of distance matrix. Required to convert cdist result form to expected pdist result form"""
    return scipy.spatial.distance.squareform(Y)


def ignore_na_pdist(*args, **kwargs):
    @wraps(scipy.spatial.distance.pdist)
    def inner(X, metric="euclidean", *, out=None, **kwargs):
        """The arguments are taken from the scipy API"""

        # No NANs present? Return scipy.spatial.distance.pdist result
        if not np.any(np.isnan(X)):
            return scipy.spatial.distance.pdist(X, metric, out=out, **kwargs)

        if metric == "cityblock":
            return convert_form(minkowski(X, X, out=out, p=1, **kwargs))
        elif metric == "euclidean":
            return convert_form(minkowski(X, X, out=out, p=2, **kwargs))
        elif metric == "cosine":
            return convert_form(cosine(X, X, out=out, **kwargs))
        elif metric == "chebyshev":
            return convert_form(chebyshev(X, X, out=out, **kwargs))
        else:
            raise NotImplementedError(
                f"NA-ignored distance {metric =} not implemented."
            )

    return inner


@ignore_na_pdist
def pdist(*args, **kwargs):
    return
