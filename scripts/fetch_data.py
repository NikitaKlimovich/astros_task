import requests
import time


""" 
Extract data from api
"""
def fetch_data(api_config):
    url = api_config['url']
    max_retries = api_config['max_retries']
    timeout = api_config['timeout']
    
    attempt = 0
    error = None
    while attempt < max_retries-1:            
        attempt += 1
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.json()
            error = f"Status {response.status_code}: {response.text}"
            if response.status_code == 429 or 500 <= response.status_code < 600:
                time.sleep(2 ** attempt)
                print(f"Attempt {attempt} failed: {error}. Retrying...")
                continue
            raise Exception(f"Critical API error: {error}")
                               
        except requests.exceptions.RequestException as e:
            error = str(e)
            print(f"Attempt {attempt} failed: {error}. Retrying...")
            time.sleep(2 ** attempt)
            
    raise Exception(f"Can't get the data from api due to max_retries: {error}")