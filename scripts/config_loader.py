import os
import yaml

def get_main_folder():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_full_config(main_folder):
    config_path = os.path.join(main_folder,'config.yml')
    return load_yaml(config_path)

def get_db_credentials(main_folder,config):
    dbt_folder = config['dbt_settings']['profile_name']
    dbt_target = config['dbt_settings']['target']
    dbt_path = os.path.join(main_folder,dbt_folder,'profiles.yml')
    dbt_settings = load_yaml(dbt_path)
    return dbt_settings[dbt_folder]['outputs'][dbt_target]