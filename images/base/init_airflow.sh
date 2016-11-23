#!/usr/bin/env bash

mysql --host=airflow-db --user=$SQL_ROOT_USER --password=$SQL_ROOT_PASSWORD --execute "CREATE DATABASE $SQL_DATABASE"
mysql --host=airflow-db --user=$SQL_ROOT_USER --password=$SQL_ROOT_PASSWORD --execute "CREATE USER $SQL_USER IDENTIFIED BY '$SQL_PASSWORD'"

mysql --host=airflow-db --user=$SQL_ROOT_USER --password=$SQL_ROOT_PASSWORD --execute "GRANT ALL PRIVILEGES ON $SQL_DATABASE.* TO '$SQL_USER'@'%'"
mysql --host=airflow-db --user=$SQL_ROOT_USER --password=$SQL_ROOT_PASSWORD --execute "FLUSH PRIVILEGES"

airflow initdb

