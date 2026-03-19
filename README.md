# API to ClickHouse Data Pipeline

This project streamlines the process of extracting data from an API and loading it into ClickHouse database using Python and dbt for transformations. The pipeline supports incremental loading, ensuring that only new data is processed during subsequent runs.

---

## Prerequisites

Ensure you have the following installed on your system:
* **Docker** 
* **Python 3.x**


### 1. Start ClickHouse Server
Run the following command to pull the ClickHouse image and start the container:

```bash
docker run -d \
  --name clickhouse-server \
  -p 8123:8123 -p 9000:9000 -p 9009:9009 \
  -e CLICKHOUSE_USER='your_username' \
  -e CLICKHOUSE_PASSWORD='your_password' \
  clickhouse/clickhouse-server:latest
```
Verification: Open http://localhost:8123/ in your browser. You should see a confirmation that the ClickHouse server is running.

### 2. Environment Setup
Install the necessary Python dependencies:

```bash
pip install -r requirements.txt
```
Open your **profile_example.yml** file in dbt project directory and **change "user" and "password" fields** to your username and password from clickhouse instance. Then **rename it to profile.yml**.

### 3. Initialize dbt
Navigate to the dbt_project folder and run dbt to create the required tables and views in ClickHouse:

```bash
cd dbt_project

# Verify the connection to ClickHouse
dbt debug --profiles-dir . 

# Run transformations to create entities
dbt run --profiles-dir . 
```
### 4. Run the Data Pipeline
Execute the main script from the project root to fetch data from the API and load it into ClickHouse:

```bash
# Change folder
cd ..

cd scripts

# Run the ingestion script
python main.py
```

### Incremental Loading

The pipeline is designed to be efficient. If new data becomes available at the API source, simply rerun the python main.py script. It will automatically detect and load only the new records without duplicating existing data.