# Pranav Minasandra
# pminasandra.github.io
# May 04, 2026

import inspect
import os
import os.path
from pathlib import Path

import config


def saveimg(obj, name, directory=config.FIGURES):
    """
    Saves given object to directory (default the FIGURES directory in config.py), with file formats chosen in config.py.
    Args:
        obj: a matplotlib object with a savefig method (plt or plt.Figure)
        name (str): the name to be given to the file, *without* extensions.
    """
    directory = Path(directory)
    dirs = [directory/f for f in config.formats]
    for dir_ in dirs:
        dir_.mkdir(exist_ok=True)

    for f in config.formats:
        obj.savefig((directory / f / name).withsuffix(f), dpi=500.0, format=f)


def sprint(*args, **kwargs):
    filename = str(inspect.stack()[1].filename)
    print(os.path.basename(filename)+":", *args, **kwargs)

