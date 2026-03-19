import json
import os
from clickhouse_connect import get_client

"""
Create a connection to clickhouse using .env file
"""
def get_connection(db_config):
    return get_client(
        host=db_config['host'], 
        username=db_config['user'], 
        password = db_config['password'],
        port=db_config['port']
    )

"""
Insert data into tables and do deduplication
"""
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