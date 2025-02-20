import logging
import os
import pandas as pd

from . import common


logging.basicConfig(level=logging.INFO)
config = common.load_config()

fs_path_extracted = config["fs_path_extracted"]
fs_path_transformed = config["fs_path_transformed"]

metadata_table = config["postgres_tables"]["metadata"]["name"]
hourly_table = config["postgres_tables"]["hourly"]["name"]

def _read_orc(date_from: str):
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), fs_path_extracted + f"open_meteo_data_{date_from}.orc")

    return pd.read_orc(filename)

def _save_transformed_metadata(pd_raw_df: pd.DataFrame):
    selected_df = pd_raw_df[["request_id", "city", "latitude", "longitude"]].drop_duplicates()
    selected_df = selected_df.reset_index(drop=True)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fs_path_transformed + f"{metadata_table}.orc")

    if os.path.exists(file_path):
        os.remove(file_path)

    logging.info(f"🗑️ Deleted existing ORC file: {file_path}")
    selected_df.to_orc(file_path, engine="pyarrow")
    logging.info(f"✅ The data of {metadata_table} was transformed")


def _save_transformed_hourly_data(pd_raw_df: pd.DataFrame):
    selected_df = pd_raw_df[["request_id", "time", "temperature_2m", "windspeed_10m", "precipitation", "relative_humidity_2m"]]
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fs_path_transformed + f"{hourly_table}.orc")

    if os.path.exists(file_path):
        os.remove(file_path)

    selected_df.to_orc(file_path, engine="pyarrow")
    logging.info(f"✅ The data of {hourly_table} was transformed")


def transform_weather_data(date_from: str):
    pd_raw_table = _read_orc(date_from)
    _save_transformed_metadata(pd_raw_table)
    _save_transformed_hourly_data(pd_raw_table)
