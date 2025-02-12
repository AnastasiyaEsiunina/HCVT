from datetime import datetime, timezone

from import_open_meteo.processor.api_data_extractor import extract_weather_data
from .processor.transformer import transform_weather_data
from .processor.db_loader import load_to_postgres
from .processor.common import load_config

config = load_config()

def extract_weather(date_from: str):
    """Extract Open Weather data"""
    extract_weather_data(date_from)
    print(f"Extracting weather data for {date_from}")

def transform_data(date_from: str):
    """Transform extracted data"""
    transform_weather_data(date_from)
    print(f"Transforming data for {date_from}")

def load_to_db(date_from: str):
    """Load data to Postgres"""
    load_to_postgres()
    print(f"Loading data to DB for {date_from}")

FUNCTIONS = {
    "extract": extract_weather,
    "transform": transform_data,
    "load": load_to_db,
}

def run(task: str, date_from: str = None):
    """Run a specific function in the pipeline."""
    if task not in FUNCTIONS:
        raise ValueError(f"Invalid task: {task}. Must be one of {list(FUNCTIONS.keys())}")

    if date_from is None:
        date_from = datetime.now(timezone.utc).isoformat()

    FUNCTIONS[task](date_from)