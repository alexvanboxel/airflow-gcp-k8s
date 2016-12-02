# airflow-gcp-k8s

## Requirements

- Cloud SQL
-- admin user with remote access
- GKE Cluster

## Preparing your configuration

### Service Account

Create a service account JSON file, and store it on the system you will run this script
from.

### Settings File

This setup uses the CloudSQL proxy, fill in the details. The root user+password is needed
to create the seperate database and user for AirFlow

```
database-init:
  proxy:
    project: my-gc-project
    zone: europe-west1
    instance: airflow-instance
  user: root
  password: "my_super_secure_password"
```

Setup a "Client ID for Web application" for Google authentication. May sure:
"Authorized redirect URIs" are set, example:
http://airflow.example.com:8080/oauth2callback?next=%2Fadmin%2F

```
auth:
  client_id: 00000000000000-aaaaaaaaaaaaaaaaaaaaa.apps.googleusercontent.com
  client_secret: aABBBBBBBBCCCCCCCCCDDDDD
  oauth_callback_route: /oauth2callback
  domain: example.com
```

Per domain, fill in the needed information: 

Remark on service key: This is the path to the JSON key on your system. It will be 
uploaded to K8S.

```
environments:
  - name: production
    namespace: default
    database:
      database: airflow
      user: airflow_production
      password: secret
    service-accounts:
      - name: service-account.json
        path: /Users/me/airflow/my-key-file.json
    git:
      branch: master
      repo-dag: airflow-dag
      repo-plugin: airflow-plugin
    staging-bucket: gs://my-bucket/airflow/libs
    logging:
      conn_id: gcp_default
      bucket: gs://my-bucket/airflow/default/logs
    webserver:
      base_url: http://airflow-dev.example.com:8080
```

Repeat the above block for all the environments you have (example, staging vs production)

## Create Airflow

You need python 2, run:

python gcp-airflow.py

and follow instructions