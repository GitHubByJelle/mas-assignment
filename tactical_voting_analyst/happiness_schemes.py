from enum import IntEnum
import numpy as np


class HappinessScheme(IntEnum):
    borda_count = 0
    linear_weight = 1
    squared_weight = 2