"""Compute distances in numpy arrays with nans"""
__version__ = "0.9.0"

from .cdist import cdist  # noqa: F401
from .pdist import pdist  # noqa: F401
from .functions import (
    chebyshev,  # noqa: F401
    cityblock,  # noqa: F401
    cosine,  # noqa: F401
    euclidean,  # noqa: F401
    minkowski,  # noqa: F401
)

SUPPORTED_METRICS = [
    "chebyshev",
    "cityblock",
    "cosine",
    "euclidean",
    "minkowski",
]
