"""
Settings to import datapath
"""

from pathlib import Path
from esupy.processed_data_mgmt import Paths, mkdir_if_missing

MODULEPATH = Path(__file__).resolve().parent
methodpath = MODULEPATH / 'methods'
datapath = MODULEPATH / 'data'

# "Paths()" are a class defined in esupy
paths = Paths()
paths.local_path = paths.local_path / 'lfg-calc-py'
outputpath = paths.local_path
emissionoutputpath = outputpath / 'Emissions'

# ensure directories exist
mkdir_if_missing(emissionoutputpath)
