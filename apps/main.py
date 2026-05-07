import sqlite3
import kagglehub
import pandas as pd
from pandas import DataFrame
from kagglehub import KaggleDatasetAdapter
from pathlib import Path

def download_and_extract_from_kagglehub(ds_path: str, ds_file_name: str, db_file_name: str) -> DataFrame | None:
    """
    Download and extract data from kagglehub
    :param ds_path: path to kaggle dataset
    :param ds_file_name: name of kaggle dataset
    :param db_file_name: name of database file
    :return: DataFrame or None
    """
    ds_name = ds_path.split("/")[-1].replace('-', '_')

    # Note: to handle error: "SSL: CERTIFICATE_VERIFY_FAILED" or no connection to the server
    try:
        # for testing
        # raise Exception

        ds_data = kagglehub.dataset_load(
            KaggleDatasetAdapter.PANDAS,
            ds_path,
            ds_file_name,
        )

        file_path = Path(db_file_name)

        # Use only one time to initialize/update data (at first time)
        if not file_path.exists():
            conn = sqlite3.connect(db_file_name)
            ds_data.to_sql(ds_name, conn, if_exists="replace", index=False)
            conn.close()
    except Exception:
        conn = sqlite3.connect(db_file_name)
        ds_data = pd.read_sql(f"SELECT * FROM {ds_name}", conn)
        conn.close()

    return ds_data
