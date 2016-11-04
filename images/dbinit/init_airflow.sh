#!/usr/bin/env bash



mysql add_user.sql
airflow initdb
mysql prepare_db.sql

