"""
Functions used to validate models
"""
from lfg_calc_py.landfill_script import landfill_capacity


def check_if_landfill_is_full(current_capacity):
    if 0 < current_capacity < landfill_capacity:
        return current_capacity
    else:
        raise ValueError("The landfill is over its maximum waste capacity")
