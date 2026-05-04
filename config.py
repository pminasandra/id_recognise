
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

formats=['png', 'pdf', 'svg']

#Miscellaneous
SUPPRESS_INFORMATIVE_PRINT = False
print(PROJECTROOT)
