# Landfill Modeling Options

## Parameters in "Default Parameters" YAML file
1. _degradable_organic_carbon_: fpo, amount of potentially degradable organic carbon in the year of
deposition, Mg C / Mg waste. Default is 0.17.
2. _degradable_organic_carbon_fraction_: fpo, fraction of the degradable organic carbon that can be 
decomposed in the anaerobic conditions of a landfill. Default is 0.5
3. _methane_content_: fpo, fraction by volume of methane in the landfill gas. Default is 0.5.
4. _methane_fraction_: fpo, fraction of degradable organic carbon that will decompose anaerobically 
into CH4. Default is 1.
5. _methane_oxidation_: bool, whether the generated methane undergoes oxidation. Default is True.
6. _methane_oxidation_fraction_: fpo, fraction of generated methane that undergoes oxidation. Default is 0.1.
7. _landfill_lifespan_: int, the number of years the landfill remains open after the waste is disposed. Also 
the number of years for which the calculation will run, if neither calc_year nor landfill_close are specified. 
Default is 100 (WARM default).

## Model parameters
1. _model_type_: required, str, YAML file format for model (single-year input vs multi-year input)
2. _use_default_model_parameters_: required, bool, whether the default parameters should be used
3. _degradable_organic_carbon_: optional, fpo, amount of potentially degradable organic carbon in the year of
deposition, Mg C / Mg waste. Required if default parameters not used.
4. _degradable_organic_carbon_fraction_: optional, fpo, fraction of the degradable organic carbon that can be 
decomposed in the anaerobic conditions of a landfill. Required if default parameters not used.
5. _methane_content_: optional, fpo, fraction by volume of methane in the landfill gas. Required if default
parameters not used.
6. _methane_fraction_: optional, fpo, fraction of degradable organic carbon that will decompose anaerobically 
into CH4. Required if default parameters not used.
7. _default_decay_rates_: required, str, source of decay rate values
   8. Barlaz: use decay rates from Barlaz literature (WARM default)
   9. IPCC: use decay rates from IPCC literature (currently not supported)
   10. False: decay rates are not imported from literature, user must provide
8. _methane_oxidation_: optional, bool, whether the generated methane undergoes oxidation. Required if default 
parameters not used.
9. _methane_oxidation_fraction_: optional, fpo, fraction of generated methane that undergoes oxidation. Required if
default parameters not used. Values above 0.1 should be supported with documentation.
10. _calc_year_: optional, the year at which the landfill gas calculation will end

## Landfill physical characteristics
1. _state_: required, str, the state where the landfill is built
2. _moisture_conditions_: required, str, annual precipitation at landfill in alignment with WARM
   1. Dry: <20 inches of precipitation per year
   3. Moderate: 20-40 inches of precipitation per year
   4. Wet: >40 inches of precipitation per year
   5. National average: weighted average based on share of waste received at each condition type
   6. Bioreactor: Water is added until the moisture content reaches 40% moisture on a
   wet weight basis
3. _LFG_recovery_: required, bool, whether landfill gas is being recovered or not
3. _LFG_collection_scenario_: required, str, efficiencies for LFG collection over the landfill life
   1. False: landfill gas not collected
   2. Typical: typical landfill gas collection scenario
   3. Worst-case: collection under EPA New Source Performance Standards
   4. Aggressive: gas collection for bioreactor operation
   5. California: gas collection scenario for California
4. _landfill_close_: optional, int, the year the landfill is expected to close and the year at which the landfill gas 
calculation will end if calc_year is not specified
10. _landfill_lifespan_: optional, int, the number of years the landfill remains open after the waste is disposed. Also 
the number of years for which the calculation will run, if neither calc_year nor landfill_close are specified. Required
if default parameters not used and neither calc_year nor landfill_close are specified.


## Waste characteristics
1. _waste_acceptance_rate_: required, dict, annual quantity of waste accepted at the landfill in metric tons/year
2. _material_ratios_: required, dict, name and fraction of each material type in the waste. Names should match 
material types in decay rate source.
3. _material_decay_rates_: optional, dict, decay rates for each of the materials in the waste. Required if Barlaz
decay rates not used.

