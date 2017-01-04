#!/usr/bin/env bash

. ./env.sh
. ./env_private.sh

cd ${base_path}/images/master_private

sed -i .b1 -E 's/airflow-master\:[\.0-9a-z]*/airflow-master:'"${version}"'/g' Dockerfile
docker build -t ${private_repo}/airflow-master:${private_version} .
gcloud docker -- push ${private_repo}/airflow-master:${private_version}

cd ${base_path}/images/worker_private

sed -i .b1 -E 's/airflow-worker\:[\.0-9a-z]*/airflow-worker:'"${version}"'/g' Dockerfile
docker build -t ${private_repo}/airflow-worker:${private_version} .
gcloud docker -- push ${private_repo}/airflow-worker:${private_version}

