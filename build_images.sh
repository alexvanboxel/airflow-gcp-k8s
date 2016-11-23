#!/usr/bin/env bash

. ./env.sh

cd ${base_path}/images/master

sed -i .b1 -E 's/airflow-base\:[\.0-9a-z]*/airflow-base:'"${base_version}"'/g' Dockerfile
sed -i .b2 -E 's/checkout\ [0-9a-f]*/checkout '"${tag}"'/g' Dockerfile
docker build -t b.gcr.io/airflow-gcp/airflow-master:${version} .
gcloud docker -- push b.gcr.io/airflow-gcp/airflow-master:${version}

cd ${base_path}/images/worker

sed -i .b1 -E 's/airflow-base\:[\.0-9a-z]*/airflow-base:'"${base_version}"'/g' Dockerfile
sed -i .b2 -E 's/checkout\ [0-9a-f]*/checkout '"${tag}"'/g' Dockerfile
docker build -t b.gcr.io/airflow-gcp/airflow-worker:${version} .
gcloud docker -- push b.gcr.io/airflow-gcp/airflow-worker:${version}

