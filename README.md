# lfg-calc-py

A landfill gas generation and emissions calculator in Python. 

Calculates material-specific annual methane generation, capture, and emissions from a single year of waste disposal over the lifespan of a landfill.

Calculates landfill gas emissions for 21 materials identified in [USEPA's Waste Reduction Model](https://www.epa.gov/waste-reduction-model), based on:
- Material-specific decay rates
- Landfill moisture conditions
- Landfill gas recovery options
- Methane oxidation

Outputs
- Results csv
- Metadata json


## Examples
Additional example code can be found in the [examples](github.com/USEPA/lfg-calc-py/tree/main/examples) folder.

## Model Documentation and Assumptions
Model assumptions are documented in the [docs](https://github.com/USEPA/lfg-calc-py/tree/main/docs/assumptions.md) folder.

## Installation
`pip install git+https://github.com/USEPA/lfg-calc-py.git@vX.X.X#egg=lfg-calc-py`

where vX.X.X can be replaced with the version you wish to install under 
[Releases](https://github.com/USEPA/lfg-calc-py/releases).


# Disclaimer
The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use.  EPA has relinquished control of the information and no longer has responsibility to protect the integrity , confidentiality, or availability of the information.  Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA.  The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or the United States Government.
