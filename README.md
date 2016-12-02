# airflow-gcp-k8s

## Requirements

### GCP minimum requirements

- Cloud SQL
-- admin user with remote access
- GKE Cluster

### Local requirements

- GCloud SDK
-- Kubernetes component installed
- Python

verify that you can connect by doing: "kubectl proxy"

## Preparing

### Service Account

Create a service account JSON file, and store it on the system you will run this script
from.

### OAuth Key

Airfow GCP for K8S uses *GSuite* authentiacation. Create a OAuth key in your project,
go to: API-Manager :: Credentials and create a key.

![OAuth1](doc/img/oauth1.png?raw=true)

It should be a web key

![OAuth1](doc/img/oauth2.png?raw=true)

Make sure "Authorized redirect URIs" are set, example:
http://airflow.example.com:8080/oauth2callback?next=%2Fadmin%2F


## Settings File

Create a file settings.yaml. You should use settings-example.yaml as a starting point.

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

Enter the details of your Outh2 key you created:

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