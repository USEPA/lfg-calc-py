"""
Examples for generating landfill emissions
"""
from lfg_calc_py import getLFGCalculations
from lfg_calc_py import LFG


methodname = "Landfill_Example_Single_Year_Acceptance"

# load locally or generates LFG emissions if does not exist locally
df_load = getLFGCalculations(methodname)

# optionally, can generate the method, will replace a local file
df_generate = LFG.generateLFG(methodname)
