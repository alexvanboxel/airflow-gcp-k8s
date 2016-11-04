# Using official python runtime base image
FROM python:2.7.12

#RUN apt-get install python-mysqldb
#RUN apk add --update alpine-sdk
#RUN apk add --update py-numpy ca-certificates
#RUN pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org numpy
RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-131.0.0-linux-x86_64.tar.gz \
    && tar xvf google-cloud-sdk-131.0.0-linux-x86_64.tar.gz \
    && rm google-cloud-sdk-131.0.0-linux-x86_64.tar.gz
# Set the application directory

ENV SYNC_REPO_DAG airflow-dag
ENV SYNC_REPO_PLUGIN airflow-plugin
ENV SYNC_STAGING_BUCKET gs://bucket/airflow/libs
ENV SYNC_BRANCH master

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/google-cloud-sdk/bin/
CMD rm -rf /home/airflow/dags \
    && mkdir -p /home/airflow/logs \
    && rm -rf /home/airflow/plugins \
    && mkdir -p /home/airflow/staging \
    && gcloud auth activate-service-account --key-file /secret/service-account.json \
    && gcloud source repos clone $SYNC_REPO_DAG /home/airflow/dags \
    && cd /home/airflow/dags && git checkout $SYNC_BRANCH \
    && gcloud source repos clone $SYNC_REPO_PLUGIN /home/airflow/plugins \
    && cd /home/airflow/plugins && git checkout $SYNC_BRANCH \
    && gsutil rsync -r $SYNC_STAGING_BUCKET /home/airflow/staging \
    && sleep infinity
