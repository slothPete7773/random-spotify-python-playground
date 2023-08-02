from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone 
import json
import requests
import configparser

DAGS_FOLDER = "/opt/airflow/dags"
DATA_FOLDER = "/opt/airflow/data"
CREDENTIALS_FOLDER = "/opt/airflow/credentials"
config = configparser.ConfigParser()
config.read(f'{CREDENTIALS_FOLDER}/env.conf')

# Define constant variables
# BUSINESS_DOMAIN = 0
# DATA = 0
LOCATION = "asia-southeast1"
PROJECT_ID = "slothpete7773-warehouse"
GCS_BUCKET = "slothpete-spotify-side-project-playground"
KEYFILE = config.get('google_service', 'gcs_service_account')

BASE_URL = "http://spotify-api:8000/spotify-api/v1"
ENDPOINT = "/me/top/tracks" # /tracks OR /artists

def _extract_data_from_server():
    # TODO: fetch data
    # TODO: save raw data as-is to file
    
    fetched_result = requests.get(f"{BASE_URL}{ENDPOINT}", timeout=10)
    # try: 
    # except requests.exceptions.RequestException as e:
    #     raise SystemExit(e)

    json_result = json.loads(fetched_result.text)

    filename = 'data.json'
    print("AAA")
    with open(f"{DATA_FOLDER}/{filename}", 'w', encoding='utf-8') as file:
        print("BBB")
        json.dump(json_result, file)

def _upload_data_to_gcs():
    # TODO: read the json file
    # TODO: upload to GCS
    pass

default_args = {
    "owner": "slothPete7773",
    "start_date": timezone.datetime(2023, 7, 1)
}

with DAG(
    dag_id="fetch_top_tracks_monthly",
    schedule="@daily",
    default_args=default_args,
    tags=["test", "fetching"]
):
    extract_data_from_server = PythonOperator(
        task_id="extract_data_from_server",
        python_callable=_extract_data_from_server
    )
    
    upload_data_to_gcs = PythonOperator(
        task_id="upload_data_to_gcs",
        python_callable=_upload_data_to_gcs
    )

    extract_data_from_server >> upload_data_to_gcs