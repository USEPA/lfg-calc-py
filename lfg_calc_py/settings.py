"""
Settings to import datapath
"""

from pathlib import Path

MODULEPATH = Path(__file__).resolve().parent
methodpath = MODULEPATH / 'methods'
datapath = MODULEPATH / 'data'
