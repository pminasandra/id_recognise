# Pranav Minasandra
# pminasandra.github.io
# 04 May 2026 (May the fourth be with you.)

"""
Based on specified sleep-site locations, gathers accelerometer data for all those
individuals in the vicinity of those specific sites for those nights. 
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config
import daynight

LOCATIONS = config.DATA / Path("metadata/locations.csv")
LOG_LL_DIST_THRESH = -5.5 # made some histograms for this

def get_and_trim_acc(animal_id, date, session):
    """
    Trim a given dataframe to the night of a specific date.
    """
    filename = (config.VEDBA_FILES / animal_id).with_suffix(".parquet")
    start, end = daynight.the_night_of(date, "evening")

    the_date = pd.to_datetime(date)
    if session == 'morning':
        the_date = the_date + pd.to_timedelta('1d')
    the_date = the_date.date()

    try:
        df = pd.read_parquet(filename)
    except FileNotFoundError:
        return
    df = df.loc[(df.timestamp > start) & (df.timestamp < end)]
    df = df.dropna()

    tdir = config.DATA / Path(f"acc_sequences/{the_date}-{session}")
    tdir.mkdir(exist_ok=True, parents=True)
    tpath = (tdir / animal_id).with_suffix(".parquet")

    print(f"Writing {tdir.name, tpath}")
    df.to_parquet(tpath)

gta_rowwise = lambda row: get_and_trim_acc(row['animal_id'], row['date'], row['session'])

def pool_all_relevant_data():
    target_acc_files_df = []
    df = pd.read_csv(LOCATIONS)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.date

    sleep_locs = pd.read_parquet(config.INDIVIDUALS_BY_NIGHT)
    sleep_locs.loc[:, 'session'] = 'babaji_bharose'

    for i in range(df.shape[0]):
        key_date = df.loc[i, 'date']
        key_session = df.loc[i, 'session']

        night_start, night_end = daynight.the_night_of(key_date, key_session)
        key_date = night_start.date()

        sleep_locs_s = sleep_locs.loc[sleep_locs['date'] == key_date, :]
        sleep_locs_s.loc[:, 'session'] = key_session
        sleep_site_loc = df.loc[i, ["sleep_site_lat", "sleep_site_long"]].to_numpy()
        sleep_site_loc = sleep_site_loc.astype(float)

        xy = sleep_locs_s[["lat", "lon"]].to_numpy().astype(float)
        dxy = (xy - sleep_site_loc)**2
        dists = dxy.sum(axis=1)
        dists = np.sqrt(dists)
        klatsch = np.log(dists+1e-10) < LOG_LL_DIST_THRESH

        target_acc_files_df.append(sleep_locs_s.iloc[klatsch])

    target_acc_files_df = pd.concat(target_acc_files_df)
    target_acc_files_df.apply(gta_rowwise, axis=1)

if __name__ == "__main__":
    pool_all_relevant_data()
