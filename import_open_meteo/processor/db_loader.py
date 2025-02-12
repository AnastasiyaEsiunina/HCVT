import os
import pandas as pd
from . import common

config = common.load_config()

fs_path_transformed = config["fs_path_transformed"]

tables = config["postgres_tables"]

def _insert_orc_to_postgres(orc_file, table_name):
    df = pd.read_orc(orc_file)

    if df.empty:
        print("ORC file is empty. No data to insert.")
        return

    engine = common.get_db_engine()

    try:
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print(f"✅ Successfully inserted {len(df)} rows into {table_name}")

    except Exception as e:
        print(f"Error inserting data: {e}")

def load_to_postgres():
    for table in tables.values():
        table_name = table["name"]
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),fs_path_transformed + table["name"] + ".orc")
        _insert_orc_to_postgres(file_path, table_name)
