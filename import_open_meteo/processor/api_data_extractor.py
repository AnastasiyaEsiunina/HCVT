import logging
from typing import Union, Any, List, Dict
import os
import requests
import uuid
import pandas as pd
import pyarrow as pa
import pyarrow.orc as orc

from . import common

logging.basicConfig(level=logging.INFO)

API_URL = common.load_config()["api_url"]
CITIES = common.load_config()["cities"]
fs_path = common.load_config()["fs_path_extracted"]
hourly_metrics = common.get_metrics()

def _fetch_weather_data(city: str, lat: float, lon: float):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": hourly_metrics,
        "timezone": "UTC"
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    # Generate a unique request ID
    request_id = int(uuid.uuid4().int % (10**18))

    return request_id, city, lat, lon, data["hourly"]

def _save_to_orc(date_from: str, data: List[Dict[str, Union[str, float, int, Any]]]):
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), fs_path + f"open_meteo_data_{date_from}.orc")
    df = pd.DataFrame(data)
    table = pa.Table.from_pandas(df)
    with pa.OSFile(filename, "wb") as f:
        orc.write_table(table, f)


def extract_weather_data(date_from: str):
    weather_records = []
    for city, coords in CITIES.items():
        req_id, city, lat, lon, hourly_data = _fetch_weather_data(city, **coords)
        logging.info(f"✅ Fetched data for {city} | Request ID: {req_id}")

        for i in range(len(hourly_data["time"])):
            weather_records.append({
                "request_id": req_id,
                "city": city,
                "latitude": lat,
                "longitude": lon,
                "time": hourly_data["time"][i],
                **{metric: hourly_data[metric][i] for metric in hourly_metrics}
            })
    _save_to_orc(date_from, weather_records)
    logging.info("✅ ORC raw data file saved successfully.")
