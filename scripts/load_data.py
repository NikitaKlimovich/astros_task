from clickhouse_connect import get_client
import requests
import json
import os
import yaml
import time


def get_etl_config():
    return load_yaml('config.yml')

def get_dbt_profile():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    profile_path = os.path.join(base_dir, 'dbt_project', 'profiles.yml')
    with open(profile_path, 'r') as f:
        config = yaml.safe_load(f)
    profile = config['dbt_project']['outputs']['dev']
    return profile

def get_connection():
    dbt_profile = get_dbt_profile()
    return get_client(host=dbt_profile['host'], username=dbt_profile['user'], password=dbt_profile['password'])

def load_data(api):
    max_retries = 5
    attempt = 0
    error = None
    while True:
        if attempt == max_retries:
            raise Exception(f"Can't get the data from api due to max_retries: {error}")
        attempt += 1
        try:
            response = requests.get(api,timeout=5)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429 or 500 <= response.status_code < 600:
                error = response.text
                time.sleep(2 ** attempt)
                continue
            else:
                 error = response.text
                 raise Exception(f"Critical error: {error}")               
        except requests.exceptions.RequestException as error:
            error = str(error)
            time.sleep(2 ** attempt)
            continue

def insert_data(data):
    client = get_connection()
    data_str = json.dumps(data)
    client.insert(database='default',table='astros',column_names=['json_data'],data=[[data_str]])
    client.command('OPTIMIZE TABLE people FINAL')
    client.close()


if __name__ == '__main__':
    config = get_etl_config()
    data = load_data(config['source_api'])
    insert_data(data, config['etl_settings'])

