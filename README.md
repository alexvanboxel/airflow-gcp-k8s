# airflow-gcp-k8s

This script will install a *Google Cloud* optimized version of Airflow on your Google
Container Engine. The images are pulled from a public accessible Container Registry.

It has the ability to generate several versions (example: production + staging) on the
same Kubernetes cluster.

It will in dags and plugins from your own cloud git repository and binaries for gcs. (
a later release will auto-sync)

For more information on Airflow go to:
  https://airflow.incubator.apache.org/

The version of Airflow is master (sometimes plus a few fixes that will get backported to
Airflow)

## Requirements

### GCP Minimum Requirements

- Cloud SQL
    - admin user with remote access
- GKE Cluster
- GSuite for authentication
- Google Git Source repository

### Local Requirements

- GCloud SDK
    - Kubernetes component installed
- Python
    - PyYAML

verify that you can connect by doing: "kubectl proxy"

## Preparing

### Source Repo

You will need 2 source repositories. One for your DAGS and one for your PLUGINS. If you name
them ```airflow-dag``` and ```airflow-plugin``` you won't need to change the settings
in the settings file later (these are the default).

A good strategy is to have production pull in ```master``` and a staging environment
 ```develop``` branch.

### Staging Bucket

This staging bucket will be downloaded to the Airflow worker. Here you can put your
binary dataflows. Create it, and remember the location, you will have to specify it in
settings.

### Service Account

Create a service account JSON file and store it on the system you will run this script
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


# Versions

base | https://github.com/apache/incubator-airflow | master
master | https://github.com/apache/incubator-airflow | google-cloud
