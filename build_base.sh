#!/usr/bin/env bash

# parse settings
base_path=`pwd`
. parse_yaml.sh
eval $(parse_yaml versions_public.yaml "version_")

cd ${base_path}/images/base
docker build -t b.gcr.io/airflow-gcp/airflow-base:${version_base_version} .
