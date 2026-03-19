from config_loader import get_full_config, get_db_credentials, get_main_folder
from fetch_data import fetch_data
from db_client import get_connection, insert_data


"""
Run the whole etl process
"""
def run_etl():
    main_folder = get_main_folder()
    config = get_full_config(main_folder)
    config_db = get_db_credentials(main_folder,config)
    config_api = config['source_api']
    config_etl = config['etl_settings']
    data = fetch_data(config_api)
    client = get_connection(config_db)
    try:
        insert_data(client, data, config_etl)
        print("Data loaded successfully")
    finally:
        client.close()

if __name__ == '__main__':
    try:
        run_etl()
    except Exception as e:
        print(f"Failed: {e}")