import numpy as np


def reaction(initial_state: np.array) -> np.array:
    """A simple exponential reaction model on a 1D grid.
    
    Args:
        initial_state: A vector representing a series of samples along a line.

    Returns:
        U: The final state after the reaction took place.
    """
    t_max = 2.469136e-6
    dt = 2.469136e-8
    k = -4.05e4

    U = initial_state

    t_cur = 0
    while t_cur + dt < t_max:
        U += k * U * dt
        t_cur += dt

    return U


if __name__ == '__main__':
    pass