from airflow import DAG
from airflow.operators.python import PythonOperator , BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import os
import boto3

S3_ENDPOINT="http://minio:9000"
S3_ACCESS_KEY="minioadmin"
S3_SECRET_KEY="minioadmin123"
MINIO_BUCKET = "staging"

def download_parquet(execution_date ,**kwargs):
    execution_date = execution_date - relativedelta(months=1)
    execution_date = execution_date.strftime("%Y-%m")
    PARQUET_URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{execution_date}.parquet"
    LOCAL_PATH = f"/tmp/data/green_tripdata_{execution_date}.parquet"
    response = requests.get(PARQUET_URL, stream=True)
    response.raise_for_status()

    with open(LOCAL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def upload_to_minio(execution_date, ti ,**kwargs):
    execution_date = execution_date - relativedelta(months=1)
    execution_date = execution_date.strftime("%Y-%m")

    MINIO_OBJECT_NAME = f"green_tripdata_{execution_date}.parquet"
    LOCAL_PATH = f"/tmp/data/green_tripdata_{execution_date}.parquet"

    s3 = boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )
    s3.upload_file(LOCAL_PATH, MINIO_BUCKET, MINIO_OBJECT_NAME)


def cleanup_parquet(execution_date, ti ,**kwargs):
    execution_date = execution_date - relativedelta(months=1)
    execution_date = execution_date.strftime("%Y-%m")

    LOCAL_PATH = f"/tmp/data/green_tripdata_{execution_date}.parquet"
    if os.path.exists(LOCAL_PATH):
        os.remove(LOCAL_PATH)


def plus_one_month(date):
    date = datetime.strptime(date, "%Y-%m")
    date = date + relativedelta(months=1)
    date = date.strftime("%Y-%m")
    return date

with DAG(
    dag_id="parquet_in_minio",
    start_date=datetime(2023,2,1),
    schedule_interval="@monthly",
    catchup=True,
    tags = ["minio","parquet"],
) as dag:

    t2 = PythonOperator(
        task_id="download_parquet",
        python_callable=download_parquet,
        retries=5,
        retry_delay=timedelta(minutes=1),
    )

    t4 = PythonOperator(
        task_id="upload_to_minio",
        python_callable=upload_to_minio,
        retries = 3,
        retry_delay = timedelta(minutes=1)
    )


    t5 = PythonOperator(
        task_id="Cleanup_parquet",
        python_callable=cleanup_parquet
    )

    t2 >> t4 >> t5