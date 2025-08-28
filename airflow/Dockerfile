
FROM apache/airflow:2.9.1-python3.10

USER root

# Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && apt-get clean

RUN mkdir -p /tmp/data && chown -R airflow: /tmp/data

USER airflow

# Установка dbt + нужного адаптера (например, PostgreSQL)
RUN pip install --no-cache-dir dbt-core dbt-postgres pandas pyarrow boto3
