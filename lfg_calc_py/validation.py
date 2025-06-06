"""
Functions used to validate models
"""
from lfg_calc_py.landfill_script import landfill_capacity

# Checking to see if landfill has reached max capacity for the year of calculation
def check_if_landfill_is_full(current_capacity):
    if 0 < current_capacity < landfill_capacity:
        return current_capacity
    else:
        raise ValueError("The landfill is over its maximum waste capacity")

# Checking to see if k is within accepted limits
def check_k(k): #TODO: update function to pull from dataframe
    if 0 < k < 0.5:
        return k
    else:
        raise ValueError("The methane generation rate constant k is outside conventional parameters")
