#!/usr/bin/env bash

if [ ! -f versions_private.yaml ]; then
    echo "No private repository set, only building public"
    exit
fi


base_path=`pwd`
. parse_yaml.sh
eval $(parse_yaml versions_public.yaml "version_")
eval $(parse_yaml versions_private.yaml "version_")


cd ${base_path}/images/master_private

sed -i .b1 -E 's/airflow-master\:[\.0-9a-z]*/airflow-master:'"${version_public_version}"'/g' Dockerfile
docker build -t ${version_private_repo}/airflow-master:${version_private_version} .
gcloud docker -- push ${version_private_repo}/airflow-master:${version_private_version}

cd ${base_path}/images/worker_private

sed -i .b1 -E 's/airflow-worker\:[\.0-9a-z]*/airflow-worker:'"${version_public_version}"'/g' Dockerfile
docker build -t ${version_private_repo}/airflow-worker:${version_private_version} .
gcloud docker -- push ${version_private_repo}/airflow-worker:${version_private_version}

