FROM python:2.7.13

RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-150.0.0-linux-x86_64.tar.gz \
    && tar xvf google-cloud-sdk-150.0.0-linux-x86_64.tar.gz \
    && rm google-cloud-sdk-150.0.0-linux-x86_64.tar.gz
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/google-cloud-sdk/bin/

ENV SYNC_REPO_DAG airflow-dag
ENV SYNC_REPO_PLUGIN airflow-plugin
ENV SYNC_STAGING_BUCKET gs://bucket/airflow/libs
ENV SYNC_BRANCH master

RUN apt-get update -y
RUN apt-get install -y git

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD python app.py

