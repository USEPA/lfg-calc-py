# Landfill Modeling Options

## Parameters in "Default Parameters" YAML file
1. _degradable_organic_carbon_: fpo, fractional amount of degradable organic carbon in the year of
deposition, Mg C / Mg waste
2. _degradable_organic_carbon_fraction_: fpo, fraction of the degradable organic carbon that can be 
decomposed
3. _methane_content_: fpo, fraction by volume of methane in the landfill gas
4. _methane_fraction_: fpo, fractional methane correction factor for aerobic decomposition in the
year of deposition

## Landfill physical characteristics
1. _moisture_conditions_: required, fpo, annual precipitation at landfill in alignment with WARM
   1. Dry: <20 inches of precipitation per year
   3. Moderate: 20-40 inches of precipitation per year
   4. Wet: >40 inches of precipitation per year
   5. National average: weighted average based on share of waste received at each condition type
   6. Bioreactor: Water is added until the moisture content reaches 40% moisture on a
   wet weight basis
2. _LFG_recovery_: required, bool, whether landfill gas is being recovered or not
3. _LFG_collection_scenario_: required, str, efficiencies for LFG collection over the landfill life
   1. False: landfill gas not collected
   2. Typical: typical landfill gas collection scenario
   3. Worst-case:
   4. Aggressive: aggressive landfill gas collection scenario
   5. California:
4. _landfill_close_: optional, int
5. _landfill_life_: optional, int

## Method YAMLs
1. _model_type_: required, bool, YAML file format for model (single-year input vs multi-year input)

LandGEM
2. _landfill_name_: optional, str, landfill name
2. _GHGRP_ID_: optional, str, landfill ID
   - **2a.** _landfill_open_: int, the year the landfill opened
   - **2b.** _landfill_close_: int, the year the landfill is expected to close
   - **2c.** _max_years_: int, the maximum number of years for which the landfill may accept waste
   - **2d.** _waste_acceptance_rate_: dict, annual quantity of waste accepted at the landfill in metric tons/year

