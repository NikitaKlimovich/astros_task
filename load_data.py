from clickhouse_connect import get_client
import requests
import json
import os
import yaml


def get_dbt_profile():
    profile_path = os.path.join(os.getcwd(), 'astros_task', 'profiles.yml')
    with open(profile_path, 'r') as f:
        config = yaml.safe_load(f)
    profile = config['astros_task']['outputs']['dev']
    return profile

def get_connection():
    dbt_profile = get_dbt_profile()
    return get_client(host=dbt_profile['host'], username=dbt_profile['user'], password=dbt_profile['password'])

def load_data(api):
    data = requests.get(api)
    return data.json()

def insert_data(client,data):
    data_str = json.dumps(data)
    client.insert(database='default',table='astros',column_names=['json_data'],data=[[data_str]])
    client.command('OPTIMIZE TABLE people FINAL')


if __name__ == '__main__':
    api = 'http://api.open-notify.org/astros.json'
    data = load_data(api)
    client = get_connection()
    insert_data(client,data)
    client.close()

