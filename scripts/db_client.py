import json
from dotenv import load_dotenv
import os
from clickhouse_connect import get_client

def get_connection(db_config):
    load_dotenv()
    return get_client(
        host=db_config['host'], 
        username=os.getenv('db_user'), 
        password = os.getenv('db_password'),
        port=db_config['port']
    )

def insert_data(client, data, etl_config):
    data_str = json.dumps(data)
    db = etl_config['database']
    raw_table = etl_config['raw_table']
    target_table_name = etl_config['target_table']['name']
    
    client.insert(
        database=db,
        table=raw_table['name'],
        column_names=raw_table['columns'],
        data=[[data_str]]
    )
    
    client.command(f'OPTIMIZE TABLE {db}.{target_table_name} FINAL')