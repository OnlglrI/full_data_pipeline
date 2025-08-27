FROM jupyter/base-notebook:python-3.11

ENV SPARK_VERSION=3.5.1 \
    HADOOP_VERSION=3 \
    SPARK_HOME=/opt/spark
USER root

# Установка Java и утилит (без curl, так как он больше не нужен)
RUN apt-get update && apt-get install -y openjdk-17-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем заранее загруженный архив Spark из контекста билда
COPY spark-3.5.1-bin-hadoop3.tgz /tmp/spark.tgz

# Распаковываем Spark
RUN tar -xzf /tmp/spark.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME} && \
    rm /tmp/spark.tgz

# Установка Python-библиотек
RUN pip install  pyspark==3.5.1 kafka-python pandas pyarrow fastparquet


# Настройка переменных среды
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$SPARK_HOME/bin:$PATH
