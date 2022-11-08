import numpy as np

CHANCE = 2
NO_ACTION = -2
NO_VALUE = np.nan


def opponent(player):
    return 1 - player
