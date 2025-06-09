# Landfill Modeling Options

## Method YAMLs
1. _landfill_name_: optional, str, landfill name
2. _GHGRP_ID_: optional, str, landfill ID used to access landfill-specific data in the EPA Greenhouse Gas Reporting Program (GHGRP) database \

If GHGRP_ID is not provided, the following are required:
   - **2a.** _landfill_open_
   - **2b.** _landfill_close_
   - **2c.** _max_years_
   - **2d.** _waste_acceptance_rate_: dict, annual quantity of waste accepted at the landfill in metric tons/year

3. _degradable_organic_carbon_:





