# Dockerfile
FROM python:3.11-slim

# Установим зависимости
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установим dbt
RUN pip install dbt-postgres==1.6.9


# Установим переменные окружения
ENV DBT_PROFILES_DIR=/dbt

# Создадим рабочую директорию
WORKDIR /dbt

# Копируем проект внутрь
COPY . /dbt

# Точка входа по умолчанию — просто запустить dbt
CMD ["tail", "-f", "/dev/null"]
