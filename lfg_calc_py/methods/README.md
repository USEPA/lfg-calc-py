# Landfill Modeling Options

## Parameters in "Default Parameters" YAML file
1. _degradable_organic_carbon_: fpo, fractional amount of degradable organic carbon in the year of
deposition, Mg C / Mg waste. Default is 0.17.
2. _degradable_organic_carbon_fraction_: fpo, fraction of the degradable organic carbon that can be 
decomposed. Default is 0.5
3. _methane_content_: fpo, fraction by volume of methane in the landfill gas. Default is 0.5.
4. _methane_fraction_: fpo, fractional methane correction factor for aerobic decomposition in the
year of deposition. Default is 1.

## Model parameters
1. _model_type_: required, str, YAML file format for model (single-year input vs multi-year input)
2. _use_default_model_parameters_: required, bool, whether the default parameters should be used
3. _degradable_organic_carbon_: optional, fpo, fractional amount of degradable organic carbon in the year of
deposition, Mg C / Mg waste. Required if default parameters not used.
4. _degradable_organic_carbon_fraction_: optional, fpo, fraction of the degradable organic carbon that can be 
decomposed. Required if default parameters not used.
5. _methane_content_: optional, fpo, fraction by volume of methane in the landfill gas. Required if default
parameters not used.
6. _methane_fraction_: optional, fpo, fractional methane correction factor for aerobic decomposition in the
year of deposition. Required if default parameters not used.
7. _default_decay_rates_: required, str, source of decay rate values
   8. Barlaz: use decay rates from Barlaz literature (WARM default)
   9. IPCC: use decay rates from IPCC literature (currently not supported)
   10. False: decay rates are not imported from literature, user must provide
8. _material_decay_rates_: optional, list, 

## Landfill physical characteristics
1. _moisture_conditions_: required, str, annual precipitation at landfill in alignment with WARM
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
   3. Worst-case: collection under EPA New Source Performance Standards
   4. Aggressive: gas collection for bioreactor operation
   5. California: gas collection scenario that complies with California state law
4. _landfill_close_: optional, int, the year the landfill closes
5. _landfill_lifespan_: required, int, the total lifespan of the landfill


## Multi-year-specific
2. _landfill_name_: optional, str, landfill name
2. _GHGRP_ID_: optional, str, landfill ID
   - **2a.** _landfill_open_: int, the year the landfill opened
   - **2b.** _landfill_close_: int, the year the landfill is expected to close
   - **2c.** _max_years_: int, the maximum number of years for which the landfill may accept waste
   - **2d.** _waste_acceptance_rate_: dict, annual quantity of waste accepted at the landfill in metric tons/year

