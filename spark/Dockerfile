FROM bitnami/spark:3.5.1

# Устанавливаем Python-библиотеки
RUN pip install pyspark kafka-python

# Скачиваем необходимые JAR-файлы напрямую в jars/
USER root

COPY ./jars/*.jar /opt/bitnami/spark/jars/

USER 1001
