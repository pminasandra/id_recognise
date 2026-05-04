
# Pranav Minasandra
# pminasandra.github.io
# 04 May 2026 (May the fourth be with you.)

"""
Simple functions to make life easier, esp handling day-night cycles
"""

import pandas as pd

def the_night_of(date, eorm):
    """
    Returns start and stop of the night of a specific timepoint.
    Args:
        date (datetime.date): the date.
        eorm (str): "evening" or "morning"
    """

    date = pd.to_datetime(date, dayfirst=True)
    eod = pd.to_timedelta('16:00:00')
    sod = pd.to_timedelta('03:00:00')
    aday = pd.to_timedelta('1d')

    if eorm == "evening":
        return date + eod, date + aday + sod
    else:
        return date - aday + eod, date + sod
