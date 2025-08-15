"""
Examples for generating landfill emissions
"""
from lfg_calc_py import getLFGCalculations
from lfg_calc_py import LFG


methodname = "Landfill_Example_Single_Year_Acceptance"

# load locally or generate LFG emissions if do not exist locally
# df = getLFGCalculations(methodname)

# generate LFG emissions
df = LFG.generateLFG(methodname)



