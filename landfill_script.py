import numpy as np
import pandas as pd
from pathlib import Path
import yaml
MODULEPATH = Path(__file__).resolve().parent
datapath = MODULEPATH / 'methods'

with open(datapath / 'Landfill_Example.yaml') as file:
    landfill_yaml = yaml.safe_load(file)

# All variable names and units are derived from USEPA's LandGEM tool.

# Defining variables from yaml

waste_rate = landfill_yaml.get("waste_acceptance_rate")
start_year = landfill_yaml.get("landfill_open")
landfill_capacity = landfill_yaml.get("landfill_capacity")
LO = landfill_yaml.get("LO")
k = landfill_yaml.get("k")

if "calc_year" in landfill_yaml:
    calc_year = landfill_yaml.get("calc_year")
elif "landfill_close" in landfill_yaml:
    calc_year = landfill_yaml.get("landfill_close")
else:
    print("ERROR: Define calc_year or landfill_close in landfill_yaml")

n = calc_year - start_year

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

# subset waste acceptance rate df to include years up-to and including calc year
waste_rate_df_subset = waste_rate_df[waste_rate_df['Year'].astype(int) <= calc_year]

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


M = 20665

# Initial methane gen
methane_total = 0.0

for i in range(0, n + 1):
    methane_annual = 0.0  # beginning annual methane is 0 before steps

    for j in np.arange(0, 1, 0.1):
        methane_annual += k * LO * (M / 10) * np.exp(-k * (i+j))

    methane_total += methane_annual  # tot methane gen
    print(f"year {i} = {methane_annual:.3E}")

# Print final computed methane generation
print(f"total methane gen: {methane_total:.3E}")

