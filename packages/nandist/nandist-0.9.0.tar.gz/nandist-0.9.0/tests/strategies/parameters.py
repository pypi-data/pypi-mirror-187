from hypothesis.strategies import composite, floats, integers


@composite
def minkowski_p(draw):
    """Draw minkowski p, which can be an integer between 1 and 5 (typical usage) or any float between zero and 1"""
    return draw(
        floats(min_value=0.001, max_value=1, exclude_min=True, exclude_max=True)
        | integers(min_value=1, max_value=5)
    )
