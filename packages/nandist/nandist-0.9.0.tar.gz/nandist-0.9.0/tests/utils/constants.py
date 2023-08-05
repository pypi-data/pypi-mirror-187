import numpy as np

EPS = np.finfo("float").eps
RELTOL = 1e-12


ZEROS_WITH_NAN = [
    np.array([0, 0, 0]),
    np.array([0, np.NAN, 0]),
    np.array([0, 0, np.NAN]),
    np.array([0, np.NAN, np.NAN]),
]

ONE_WITH_NAN = [
    np.array([1, 0, 0]),
    np.array([1, np.NAN, 0]),
    np.array([1, np.NAN, np.NAN]),
]
