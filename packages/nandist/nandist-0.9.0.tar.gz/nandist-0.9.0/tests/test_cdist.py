"""Test cdist functions. There is no need to test nandist.pdist because it calls cdist under the hood."""

from hypothesis.strategies import integers
from hypothesis import given
from .strategies.arrays import normal_arrays, nan_arrays
from .utils.weights import weights_from_array, pseudoweights_from_factor
from .strategies.parameters import minkowski_p
from .utils.constants import EPS, RELTOL, ZEROS_WITH_NAN, ONE_WITH_NAN
import math

import pytest
import numpy as np
import scipy
import nandist


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(X=normal_arrays(), p=minkowski_p())
def test_cdist_equivalent(X, p, metric):
    """Test whether nandist.cdist returns the same results as the scipy.spatial.distance.cdist when no NaNs are in the
    arrays"""
    a, b, w = X[0], X[1], X[2]

    w = weights_from_array(w)

    XA, XB = np.array([a]), np.array([b])

    kwargs = {"metric": metric, "w": w}

    if metric == "minkowski":
        kwargs = {**kwargs, "p": p}

    try:
        Y_expected = scipy.spatial.distance.cdist(XA, XB, **kwargs)
    except ZeroDivisionError:
        assert True
        return

    Y_result = nandist.cdist(XA, XB, **kwargs)
    assert np.array_equal(Y_result, Y_expected, equal_nan=True)


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(X=nan_arrays(), p=minkowski_p())
def test_self_distance_is_zero(X, p, metric):
    """Test whether distance to self is zero, even if there are NaNs present"""
    XA, w = np.array([X[0]]), X[2]
    w = weights_from_array(w)

    # Keyword arguments
    kwargs = {"metric": metric, "w": w}

    if metric == "minkowski":
        kwargs = {**kwargs, "p": p}

    # Positional arguments
    args_nandist = (XA, XA)
    idx_nan = np.isnan(XA)
    args_scipy = (np.array([XA[~idx_nan]]), np.array([XA[~idx_nan]]))

    # scipy distance may not be calculable due to division by zero. In that case, return early.
    try:
        Y_expected = scipy.spatial.distance.cdist(*args_scipy, **kwargs)
    except ZeroDivisionError:
        assert True
        return

    # Calculate nandist distance
    Y_result = nandist.cdist(*args_nandist, **kwargs)

    # Test equivalence in the presence of NaNs
    if np.array_equal(Y_result, Y_expected, equal_nan=True):
        assert True
        return

    # Distance may not be exactly the same, but very close to zero
    distance_is_nearly_zero = math.isclose(Y_result[0][0], 0, abs_tol=EPS)
    assert distance_is_nearly_zero


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(X=nan_arrays(), p=minkowski_p())
def test_single_vector_nan_distance_weighted(X, p, metric):
    """Test the nandist distance for single vectors.
    This should equal the non-nan distance when the nan components are removed"""
    a, b, w = X
    w = weights_from_array(w)

    kwargs = {}
    if metric == "minkowsi":
        kwargs = {"p": p}

    # Create XA, XB, XAh and XBh
    idx_nan = np.isnan(a) | np.isnan(b)
    XA, XB = np.array([a]), np.array([b])
    XAh, XBh = np.array([a[~idx_nan]]), np.array([b[~idx_nan]])

    wh = None
    if w is not None:
        wh = w[~idx_nan]

    # All NANs? Return 0 as expected distance
    try:
        if XAh.shape == (0,):
            Y_expected = np.array([[0]])
        else:
            Y_expected = scipy.spatial.distance.cdist(
                XAh, XBh, metric=metric, w=wh, **kwargs
            )
    # Expected distance incalculable? Return early
    except ZeroDivisionError:
        assert True
        return

    Y_result = nandist.cdist(XA, XB, metric=metric, w=w, **kwargs)
    assert np.allclose(Y_result, Y_expected, equal_nan=True, atol=EPS)


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(X=nan_arrays(), p=minkowski_p())
def test_single_vector_nan_distance_unweighted(X, p, metric):
    """Test the nandist distance for single vectors.
    This should equal the non-nan distance when the nan components are removed"""
    a, b, _ = X

    # Create XA, XB, XAh and XBh
    idx_nan = np.isnan(a) | np.isnan(b)
    XA, XB = np.array([a]), np.array([b])
    XAh, XBh = np.array([a[~idx_nan]]), np.array([b[~idx_nan]])

    wh = None

    kwargs = {}
    if metric == "minkowski":
        kwargs = {**kwargs, "p": p}

    # All NANs? Return 0 as expected distance
    try:
        if XAh.shape == (0,):
            Y_expected = np.array([[0]])
        else:
            Y_expected = scipy.spatial.distance.cdist(
                XAh, XBh, metric=metric, w=wh, **kwargs
            )
    except ZeroDivisionError:
        assert True
        return

    Y_result = nandist.cdist(XA, XB, metric=metric, **kwargs)
    assert np.allclose(Y_result, Y_expected, atol=EPS, equal_nan=True)


@pytest.mark.parametrize("a", ZEROS_WITH_NAN)
@pytest.mark.parametrize("b", ONE_WITH_NAN)
@pytest.mark.parametrize("p", [0.1, 0.5, 1, 2, 3, 4])
@given(w_factor=integers(min_value=1, max_value=100))
def test_weighted_minkowski(a, b, w_factor, p):
    """Test weighted minkowski assuming vector a is 1 at position 0 and zero elsewhere; b is zero everywhere except for
    positions where it is NaN"""

    XA, XB = np.array([a]), np.array([b])

    # Construct weights array
    w = pseudoweights_from_factor(w_factor=w_factor, n=XA.shape[1])

    # Calculate distance
    Y = nandist.cdist(XA, XB, "minkowski", w=w, p=p)

    assert (Y[0][0] - w[0] ** (1 / p)) / Y[0][0] < RELTOL
