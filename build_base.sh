#!/usr/bin/env bash

. ./env.sh

cd ${base_path}/images/base
docker build -t b.gcr.io/airflow-gcp/airflow-base:${base_version} .

#docker build --pull --no-cache -t b.gcr.io/airflow-gcp/airflow-db:1.8.0.alpha.10 .
