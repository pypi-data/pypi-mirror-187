import pytest
import numpy as np
import math
import scipy
import nandist
from hypothesis import given

from .strategies.arrays import normal_arrays, nan_arrays
from .strategies.parameters import minkowski_p
from .utils.weights import weights_from_array
from .utils.constants import EPS


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(X=nan_arrays(), p=minkowski_p())
def test_self_distance_is_zero(X, metric, p):
    """Test whether vector distance to self is (close to) zero"""
    u, _, w = X
    w = weights_from_array(w)

    nandist_f = getattr(nandist, metric)

    kwargs = {"u": u, "v": u, "w": w}

    if metric == "minkowski":
        kwargs = {**kwargs, "p": p}

    y = nandist_f(**kwargs)

    assert math.isclose(y, 0, rel_tol=1e-8, abs_tol=1e-12)


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(X=nan_arrays(), p=minkowski_p())
def test_metric(X, p, metric):
    """Test whether nancist.euclidean gives the same distance as scipy.spatial.distance.euclidean when the components
    containing NaN have been removed from the vector"""

    scipy_f = getattr(scipy.spatial.distance, metric)
    nandist_f = getattr(nandist, metric)

    u, v, w = X
    w = weights_from_array(w)

    idx_nan = np.isnan(u) | np.isnan(v)
    uh, vh = u[~idx_nan], v[~idx_nan]

    wh = None
    if w is not None:
        wh = w[~idx_nan]

    # Numpy will do some checks on the arrays which might fail.
    # In that case, we can let the test assert as True
    try:
        if metric == "minkowski":
            Y_expected = scipy_f(uh, vh, w=wh, p=p)
        else:
            Y_expected = scipy_f(uh, vh, w=wh)
    except ValueError:
        # Dummy pass
        assert True
    except ZeroDivisionError:
        # Dummy pass
        assert True
    else:
        if metric == "minkowski":
            Y_result = nandist_f(u, v, w=w, p=p)
        else:
            Y_result = nandist_f(u, v, w=w)

        if np.isnan(Y_result) and np.isnan(Y_expected):
            assert True
        else:
            assert math.isclose(Y_result, Y_expected, abs_tol=EPS)


@given(X=nan_arrays(), p=minkowski_p())
def test_minkowski(X, p):
    """Test whether nandist.minkowski returns expected result by comparing the distance calculated between vectors that
    contain at least one NaN to the distance calculated by the same vectors where the components containing the NaN are
    removed"""
    u, v, w = X
    w = weights_from_array(w)

    idx_nan = np.isnan(u) | np.isnan(v)
    uh, vh = u[~idx_nan], v[~idx_nan]

    wh = None
    if w is not None:
        wh = w[~idx_nan]

    try:
        Y_expected = scipy.spatial.distance.minkowski(uh, vh, w=wh, p=p)
    except ValueError:
        assert True
    else:
        Y_result = nandist.minkowski(u, v, w=w, p=p)

        assert math.isclose(Y_result, Y_expected, abs_tol=EPS)


@given(X=normal_arrays())
def test_euclidean_equivalence(X):
    """Assert that nandist.euclidean returns the same as scipy.spatial.distance.euclidean when no NaNs are present
    in the input vectors"""
    u, v, w = X

    w = weights_from_array(w)

    try:
        Y_expected = scipy.spatial.distance.euclidean(u=u, v=v, w=w)
    except ValueError:
        # Numpy does some checking that could raise a ValueError for some generated arrays; ignore these.
        assert True
    else:
        Y_result = nandist.euclidean(u=u, v=v, w=w)
        assert math.isclose(Y_expected, Y_result, abs_tol=EPS)


@given(X=normal_arrays(), p=minkowski_p())
def test_minkowski_equivalence(X, p):
    """Assert that nandist.minkowski returns the same as scipy.spatial.distance.minkowski when no NaNs are present
    in the input vectors"""
    u, v, w = X

    w = weights_from_array(w)

    try:
        Y_expected = scipy.spatial.distance.minkowski(u=u, v=v, w=w, p=p)
    except ValueError:
        # Numpy does some checking that could raise a ValueError for some generated arrays; ignore these.
        assert True
    else:
        Y_result = nandist.minkowski(u=u, v=v, w=w, p=p)
        assert math.isclose(Y_result, Y_expected, abs_tol=EPS)
