#!/usr/bin/env bash

docker build --pull --no-cache -t b.gcr.io/airflow-gcp/airflow-db:1.8.0.alpha.6 .
