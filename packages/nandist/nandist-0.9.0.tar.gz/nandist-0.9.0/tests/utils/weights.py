import numpy as np
from numpy.linalg import norm


def pseudoweights_from_factor(w_factor: float, n: int, idx: int = 0):
    """Return pseudoweights array such that the first element is w_factor larger than the rest of the elements.
    These are pseudo-weights because the sum of all weights does not add up to 1."""
    w = np.ones(n, dtype="float")
    if n == 1:
        w[idx] == 1
        return w

    # Construct weight array with w_factor the factor the first component weighs vs the rest of the componentes
    w[idx] = w_factor
    return w


def weights_from_array(w):
    """Construct normalized weights array from an arbitrary array"""

    # Positive weights only
    w = np.abs(w)

    # Replace NaN with 0
    idx_nan = np.isnan(w)
    w[idx_nan] = 1

    # Array contains the same value
    if len(set(w)) == 1:
        return None

    # Normalize
    w /= norm(w, 1)

    return w
