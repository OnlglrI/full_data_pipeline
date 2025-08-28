from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor
from datetime import datetime, timedelta
import pandas as pd
import boto3
import os
from sqlalchemy import create_engine
from io import BytesIO
from dateutil.relativedelta import relativedelta

MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"
MINIO_BUCKET = "staging"

POSTGRES_CONN_URI = "postgresql+psycopg2://airflow:airflow@postgres:5432/green_taxi"
POSTGRES_SCHEMA = "staging"

CSV_TRACKING_FILE = "/opt/airflow/data/downloaded_to_postgres.csv"  # локально


def check_new_file(**context):
    s3 = boto3.client(
        "s3",
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=MINIO_BUCKET, Prefix="green_tripdata_")

    all_files = []
    for page in pages:
        for obj in page.get("Contents",[]):
            all_files.append(obj['Key'])

    if os.path.exists(CSV_TRACKING_FILE):
        df = pd.read_csv(CSV_TRACKING_FILE)
        already_loaded = set(df["filename"])
    else:
        already_loaded = set()

    new_files = list(set(all_files) - already_loaded)

    if new_files:
        context["ti"].xcom_push(key="new_files", value=new_files)
        return True
    else:
        return False

def load_parquet_to_postgres(execution_date, **context):
    new_files = context["ti"].xcom_pull(key="new_files")
    if not new_files:
        return

    execution_date = execution_date.replace(day=1)

    s3 = boto3.client(
        "s3",
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    engine = create_engine(POSTGRES_CONN_URI)

    loaded_records = []
    for file in new_files:
        obj = s3.get_object(Bucket=MINIO_BUCKET, Key=file)
        df = pd.read_parquet(BytesIO(obj["Body"].read()))

        year = file.split('_')[-1].split('.')[0].split('-')[0]
        table_name = f"green_tripdata_{year}"

        df.to_sql(
            table_name,
            engine,
            schema=POSTGRES_SCHEMA,
            if_exists="append",
            index=False
        )
        loaded_records.append(file)
        print(f"{file} → {POSTGRES_SCHEMA}.{table_name} успешно загружен.")

        os.makedirs("/opt/airflow/data", exist_ok=True)
        df_csv = pd.DataFrame([{"filename": file}])
        if os.path.exists(CSV_TRACKING_FILE):
            df_csv.to_csv(CSV_TRACKING_FILE, mode="a", index=False, header=False)
        else:
            df_csv.to_csv(CSV_TRACKING_FILE, index=False)

with DAG(
    dag_id="minio_to_postgres",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    default_args={
        "owner":"airflow",
        "retries":1,
        "retry_delay":timedelta(minutes=3)
    }
) as dag:

    wait_for_new_file = PythonSensor(
        task_id="wait_for_new_file",
        python_callable=check_new_file,
        poke_interval=60,
        timeout=300,
        mode="poke"
    )

    load_and_track = PythonOperator(
        task_id="load_and_track",
        python_callable=load_parquet_to_postgres,
        provide_context=True,
    )

    wait_for_new_file >> load_and_track