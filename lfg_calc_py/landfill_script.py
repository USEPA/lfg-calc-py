import numpy as np
import pandas as pd
import yaml
from sympy import exp, symbols
from lfg_calc_py.settings import methodpath, datapath
#from lfg_calc_py.ghgrp import return_ghgrp_data

with open(datapath/'IPCC_Waste_specific_k-values.csv') as file:
    waste_specific_k_df = pd.read_csv(file)

with open(methodpath / 'Landfill_Example.yaml') as file:
    landfill_yaml = yaml.safe_load(file)

# All variable names and units are derived from USEPA's LandGEM tool.

# Defining variables from yaml

waste_rate = landfill_yaml.get("waste_acceptance_rate")
start_year = landfill_yaml.get("landfill_open")
landfill_capacity = landfill_yaml.get("landfill_capacity")
degradable_organic_carbon = landfill_yaml.get("degradable_organic_carbon")
degradable_organic_carbon_fraction = landfill_yaml.get("degradable_organic_carbon_fraction")
k = landfill_yaml.get("k")
methane_correction_factor = landfill_yaml.get("methane_correction_factor")
methane_content = landfill_yaml.get("methane_content")

if "calc_year" in landfill_yaml:
    calc_year = landfill_yaml.get("calc_year")
elif "landfill_close" in landfill_yaml:
    calc_year = landfill_yaml.get("landfill_close")
else:
    print("ERROR: Define calc_year or landfill_close in landfill_yaml")

T = calc_year - start_year
x = symbols('x')

# empty dictionary
waste_rate_split = {}

for key, value in waste_rate.items():
    # if data is provided as a range, split the range and add waste acceptance for each year to new dictionary
    if "-" in key:
        y1, y2 = map(int, key.split("-"))
        for year in range(y1, y2 + 1):
            waste_rate_split[str(year)] = value
    # else if entry is a single value, append to new dictionary as-is
    else:
        waste_rate_split[str(key)] = value


# convert expanded dictionary into df
waste_rate_df = pd.DataFrame(waste_rate_split.items(), columns = ['Year', 'WasteAcceptanceRate'])
# set datatypes
waste_rate_df['Year'] = waste_rate_df['Year'].astype(int)
waste_rate_df['WasteAcceptanceRate'] = waste_rate_df['WasteAcceptanceRate'].astype(float)

# subset waste acceptance rate df to include years up-to and including calc year
waste_rate_df_subset = waste_rate_df[waste_rate_df['Year'] <= calc_year-1]

# To get waste acceptance rates for years of calculation
current_capacity = sum(waste_rate_df_subset['WasteAcceptanceRate'])

# Parameters and checks

# Checking to see if landfill has reached max capacity for the year of calculation
def check_if_landfill_is_full(current_capacity):
    if 0 < current_capacity < landfill_capacity:
        return current_capacity
    else:
        raise ValueError("The landfill is over its maximum waste capacity")

# Checking to see if k is within accepted limits
def check_k(k):
    if 0 < k < 0.5:
        return k
    else:
        raise ValueError("The methane generation rate constant k is outside conventional parameters")

# Calling the parameter functions
check_if_landfill_is_full(current_capacity)
check_k(k)

def return_waste_acceptance(year):
    """
    Return the waste acceptance for a year, return 0 value if no waste managed that year
    :param year:
    :return:
    """
    try:
        return float(waste_rate_df_subset.loc[
                         waste_rate_df_subset['Year'] == year, 'WasteAcceptanceRate'].values[0])
    except IndexError:
        return 0

# Methane calculation
methane_total = 0.0
methane_annual = 0.0
methane_df = pd.DataFrame()

# Range upper limit in summation is 1 higher than IPCC equation
# due to range function in Python

for x in range(0, T):
    methane_annual = (return_waste_acceptance(start_year + x)
    * methane_correction_factor
    * degradable_organic_carbon
    * degradable_organic_carbon_fraction
    * methane_content
    * 16/12
    * (exp(-k*(T-x-1)) - exp(-k*(T-x)))
    )

    methane_total += methane_annual
    print(f"{methane_total} for {start_year + x}")

print(f"Total methane generation in year {calc_year}: {methane_total} tonnes CH4")


