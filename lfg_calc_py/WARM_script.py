import pandas as pd
import yaml
from sympy import exp, symbols
from lfg_calc_py.settings import methodpath, datapath, emissionoutputpath
# from lfg_calc_py.validation import check_if_landfill_is_full


# def return_method_yaml(method_name):
#     with open(f"{methodpath}/{method_name}.yaml") as file:
#         method_yaml = yaml.safe_load(file)
#     return method_yaml

method_name = 'Landfill_Example_Material_Specific'

with open(f"{methodpath}/{method_name}.yaml") as file:
    method_yaml = yaml.safe_load(file)


# All variable names and units are derived from USEPA's LandGEM tool.

# Defining variables from yaml

waste_rate = method_yaml.get("waste_acceptance_rate")
landfill_life = method_yaml.get("landfill_life")
landfill_capacity = method_yaml.get("landfill_capacity")
degradable_organic_carbon = method_yaml.get("degradable_organic_carbon")
degradable_organic_carbon_fraction = method_yaml.get("degradable_organic_carbon_fraction")
material_ratios = method_yaml.get("material_ratios")
material_decay_rates = method_yaml.get("material_decay_rates")
methane_correction_factor = method_yaml.get("methane_correction_factor")
methane_content = method_yaml.get("methane_content")
moisture_conditions = method_yaml.get("moisture_conditions")
LFG_recovery = method_yaml.get("LFG_recovery")
LFG_collection_scenario = method_yaml.get("LFG_collection_scenario")

# todo: modify to account for "false"/no default data/all user input data
def load_default_decay_rates():
    source = method_yaml.get("default_k_values")
    if source == "IPCC":
        path = datapath/'IPCC_Waste_specific_k-values.csv'
    elif source == "Barlaz":
        path = datapath/'WARM_Barlaz_Material_Decay_Rates.csv'
    with open(path) as file:
        decay_rates = pd.read_csv(file)
    return decay_rates

# WARM LFG collection efficiencies by year
path = datapath/'LFG_collection_scenarios.csv'
with open(path) as file:
    yearly_lfg_collection_efficiencies = pd.read_csv(file)
# todo: combine with material-specific collection efficiencies

# WARM material-specific LFG collection efficiencies
path = datapath/'WARM_GasCollectionEfficiencies_v1.csv'
with open(path) as file:
    material_lfg_collection_efficiencies = pd.read_csv(file)

# Defining calc_year
if "calc_year" in method_yaml:
    calc_year = method_yaml.get("calc_year")
elif "landfill_close" in method_yaml:
    calc_year = method_yaml.get("landfill_close")
else:
    calc_year = 2024
    #todo: automatically update to current date

## Calling functions ##
load_default_decay_rates()


T = landfill_life
x = symbols('x')

# empty dictionary
waste_rate_split = {}
material_ratio_split = {}

for key, value in waste_rate.items():
    # if data is provided as a range, split the range and add waste acceptance for each year to new dictionary
    if "-" in str(key):
        y1, y2 = map(int, key.split("-"))
        for year in range(y1, y2 + 1):
            waste_rate_split[str(year)] = value
    # else if entry is a single value, append to new dictionary as-is
    else:
        waste_rate_split[str(key)] = value

for key, value in material_ratios.items():
    # if data is provided as a range, split the range and add waste acceptance for each year to new dictionary
    if "-" in key:
        y1, y2 = map(int, key.split("-"))
        for year in range(y1, y2 + 1):
            material_ratio_split[str(year)] = value
    # else if entry is a single value, append to new dictionary as-is
    else:
        material_ratio_split[str(key)] = value
#TODO: ensure the key corresponds to year, not waste type

# convert expanded dictionary into df
waste_rate_df = pd.DataFrame(waste_rate_split.items(), columns = ['Year', 'WasteAcceptanceRate'])
material_ratio_df = pd.DataFrame(material_ratios.items(), columns = ['Waste Type', 'Waste Fraction'])
#TODO: add third column to material ratio df for year?


# set datatypes
waste_rate_df['Year'] = waste_rate_df['Year'].astype(int)
waste_rate_df['WasteAcceptanceRate'] = waste_rate_df['WasteAcceptanceRate'].astype(float)

# subset waste acceptance rate df to include years up-to and including calc year
waste_rate_df_subset = waste_rate_df[waste_rate_df['Year'] <= calc_year-1]

# add material ratios
material_type_list = list(material_ratios.keys())

#
material_decay_rates_df = pd.DataFrame(material_decay_rates.items(),
                                       columns = ['Waste Type', 'Material Decay Rate'])
# Remove excess moisture scenarios
conditions_list = ['Dry','Moderate','Wet','Bioreactor','National Average']
mc_list = [moisture_conditions]
if moisture_conditions in conditions_list:
    conditions_list = [x for x in conditions_list if x not in mc_list]
    material_lfg_collection_efficiencies = material_lfg_collection_efficiencies.drop(
        columns = conditions_list)
else:
    raise ValueError("The moisture conditions are outside the specified range")

scenario_list = ['Typical operation', 'Worst-case', 'Aggressive', 'California']
sc_list = [LFG_collection_scenario]
if LFG_collection_scenario in scenario_list:
    scenario_list = [x for x in scenario_list if x not in sc_list]
    material_lfg_collection_efficiencies = material_lfg_collection_efficiencies[~material_lfg_collection_efficiencies
    ['Scenario'].isin(scenario_list)]
else:
    material_lfg_collection_efficiencies = material_lfg_collection_efficiencies.drop(columns = 'Scenario')

# Parameters and checks

# TODO: add check to match waste type of methane gen values with material ratios (so they align)



# Calling the parameter functions
# check_if_landfill_is_full(current_capacity)
# check_k(k)

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

def return_material_decay_rates(material):
    """
    Return the methane generation rate for a waste type
    :return:
    """
    return float(material_decay_rates_df.loc[
                     material_decay_rates_df['Waste Type'] == material, 'Material Decay Rate'].values[0])

def return_material_ratio(material):
    """
    Return the fraction of a material in a waste
    :return:
    """
    return float(material_ratio_df.loc[
            material_ratio_df['Waste Type'] == material, 'Waste Fraction'].values[0])


def return_gas_collection_efficiency(material):
    """
    Return gas collection efficiency by material and year
    :return:
    """
    return float()
    # load csv of material by year efficiencies
    # subset by material
    # return for year

    return df

# todo: first year emissions out of landfill should be 0

# def calculate_landfill_emissions(method_name):
# Methane calculation
# methane_total = 0.0
methane_annual = 0.0
methane_df = pd.DataFrame()

# empty data
emissions_data = []
# Initial cumulative methane totals are 0 for each material
methane_totals = {material: 0.0 for material in material_type_list}

# Range upper limit in summation is 1 higher than IPCC equation
# due to range function in Python
for x in range(0, T):
    row = {"Year": calc_year + x}
    for material in material_type_list: #TODO: make this iterate for each material type? Connect material ratio
        # and generation rates? Turn methane_annual into a dataframe to separate out contributions by waste type?
        methane_annual = (
                return_material_ratio(material)
                * (return_waste_acceptance(calc_year + x)
                   * methane_correction_factor
                   * degradable_organic_carbon
                   * degradable_organic_carbon_fraction
                   * methane_content
                   * 16/12
                   * (exp(-return_material_decay_rates(material) * (T - x - 1))
                      - exp(-return_material_decay_rates(material) * (T - x)))
                   )
        )
        methane_totals[material] += methane_annual  # cumulative total for material
        row[f"{material} Methane Annual"] = methane_annual  # annual value
        row[f"{material} Methane Total"] = methane_totals[material]  # cumulative
        # todo: add new row item for unit
        # todo: new columns for summed materials

    emissions_data.append(row)  # Append row data to list


df = pd.DataFrame(emissions_data)
df = df.assign(Unit="Metric Tons")
# todo: update file name to be method file name
df.to_csv(f"{emissionoutputpath}/{method_name}.csv", index=False)

    # return df



# print(f"Total methane generation in year {calc_year}: {methane_total} tonnes CH4")


