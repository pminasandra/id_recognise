# Pranav Minasandra
# pminasandra.github.io
# 04 May 2026 (May the fourth be with you.)

"""
Reads in accelerometer data, converts to VeDBA sequences, other preprocessing.
"""

from pathlib import Path

import accutils
import pandas as pd

import config

ACC_DIR = config.DATA / "acc_sequences"
CONTINUOUS_ACC_DIR = config.DATA / "continuous_vedba_seq"
SESSION_DETAILS = config.DATA / "metadata" / "locations.csv"
SESSION_METADATA = pd.read_csv(SESSION_DETAILS)

def filter_to_continuous(df, max_gap_s=3):
    """
    Extract the longest approximately continuous chunk of accelerometer data.

    Args:
        df (pd.DataFrame):
            Must contain a 'Timestamp' column of dtype datetime64.
        max_gap_ms (int):
            Maximum allowed gap between consecutive samples before a new
            chunk is started.

    Returns:
        pd.DataFrame:
            Copy of the longest continuous chunk.
    """
    df = df.copy()

    diff = df['timestamp'].diff()
    chunks = (diff > pd.Timedelta(seconds=max_gap_s)).cumsum()
    chunk_lengths = chunks.value_counts()
    longest_chunk = chunk_lengths.idxmax()

    dfs = df[chunks == longest_chunk].copy()
    if dfs.shape[0] > 100:
        dfs = dfs.reset_index()
        ts = dfs.timestamp.to_list()
        return dfs
    return None

def _process(fname):
    df = pd.read_parquet(fname)
    df = filter_to_continuous(df)

    if df is None:
        return

    df['vedba'] = accutils.feature_ext.dbas.vedba_vals(df)
    df = accutils.feature_ext.secondwise_mean(df)

    df.to_parquet(CONTINUOUS_ACC_DIR / fname.parent.name / fname.name)

def filter_entire_session(dirname):
    """
    Take contents of folder, save only continuous acc portion.
    """
    parquet_files = (ACC_DIR / dirname).glob("*.parquet")
    for pfile in parquet_files:
        _process(pfile)

if __name__ == "__main__":
    CONTINUOUS_ACC_DIR.mkdir(exist_ok=True)

    to_use_sessions = SESSION_METADATA.acc_continuous == 1
    SESSION_METADATA = SESSION_METADATA[to_use_sessions]
    SESSION_METADATA['date'] = pd.to_datetime(SESSION_METADATA['date'], dayfirst=True).dt.date
    SESSION_METADATA['dirname'] = SESSION_METADATA['date'].astype(str) +\
                                    "-" +\
                                    SESSION_METADATA['session'] 
    SESSION_METADATA['dirname'] = SESSION_METADATA['dirname'].map(Path)
    create_dir = lambda dirname: (CONTINUOUS_ACC_DIR/dirname).mkdir(exist_ok=True)

    SESSION_METADATA['dirname'].apply(create_dir)
    SESSION_METADATA['dirname'].apply(filter_entire_session)
