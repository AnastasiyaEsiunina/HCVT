import os
import yaml
from sqlalchemy import create_engine

def load_config():
    yaml_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.yml")
    with open(yaml_file, "r") as file:
        return yaml.safe_load(file)


def get_db_engine():
    config = load_config()["database"]
    db_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
    engine = create_engine(db_url)

    return engine
