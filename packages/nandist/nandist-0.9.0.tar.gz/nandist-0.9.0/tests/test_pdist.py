"""Tests for nandist.pdist. Only checks for equivalence to scipy.spatial.pdist.
Numerical tests are implemented in test_cdist.py, because nandist.pdist calls nandist.cdist under the hood."""

import pytest
import scipy
import numpy as np
import nandist
from hypothesis import given
from .utils.weights import weights_from_array
from .strategies.arrays import normal_arrays


@pytest.mark.parametrize("metric", nandist.SUPPORTED_METRICS)
@given(X=normal_arrays())
def test_pdist_equivalent(X, metric):
    """Test whether the overloaded method `cdist` returns the same results as the original method when an array does not
    contain NaNs"""
    X, w = X[:2], X[2]

    w = weights_from_array(w)

    try:
        Y_expected = scipy.spatial.distance.pdist(X, metric=metric, w=w)
    except ZeroDivisionError:
        assert True
        return

    Y_result = nandist.pdist(X, metric=metric, w=w)
    assert np.array_equal(Y_result, Y_expected, equal_nan=True)
