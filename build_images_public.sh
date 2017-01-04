#!/usr/bin/env bash

base_path=`pwd`
. parse_yaml.sh
eval $(parse_yaml versions_public.yaml "version_")

cd ${base_path}/images/master

sed -i .b1 -E 's/airflow-base\:[\.0-9a-z]*/airflow-base:'"${version_base_version}"'/g' Dockerfile
sed -i .b2 -E 's/checkout\ [0-9a-f]*/checkout '"${version_public_tag}"'/g' Dockerfile
docker build -t b.gcr.io/airflow-gcp/airflow-master:${version_public_version} .
gcloud docker -- push b.gcr.io/airflow-gcp/airflow-master:${version_public_version}

cd ${base_path}/images/worker

sed -i .b1 -E 's/airflow-base\:[\.0-9a-z]*/airflow-base:'"${version_base_version}"'/g' Dockerfile
sed -i .b2 -E 's/checkout\ [0-9a-f]*/checkout '"${version_public_tag}"'/g' Dockerfile
docker build -t b.gcr.io/airflow-gcp/airflow-worker:${version_public_version} .
gcloud docker -- push b.gcr.io/airflow-gcp/airflow-worker:${version_public_version}

