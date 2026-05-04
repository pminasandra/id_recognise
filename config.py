
# Pranav Minasandra
# pminasandra.github.io
# May 04, 2026

import os
from pathlib import Path
import sys


#Directories
try:
    PROJECTROOT = open(".cw", "r").read().rstrip()
except FileNotFoundError:
    PROJECTROOT =Path(sys.argv[0]).absolute().parent.parent
DATA = PROJECTROOT / "Data"
FIGURES = PROJECTROOT/ "Figures"

SERVER_LOC = Path("/home/pranav/mpi-dir")
INDIVIDUALS_BY_NIGHT = SERVER_LOC/Path("EAS_shared/baboon/working/data/processed/2025/gps/individual_night_locations.parquet")
VEDBA_FILES = SERVER_LOC / Path("EAS_shared/baboon/working/data/processed/2025/acc/acc_v0")

#Miscellaneous
formats=['png', 'pdf', 'svg']
SUPPRESS_INFORMATIVE_PRINT = False
