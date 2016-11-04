import ConfigParser
import io
import json
from subprocess import PIPE, Popen

import yaml

x_config = {'kind': 'ConfigMap',
            'data': {'project': 'vex-eu-cloud-sql-001', 'instance': 'airflow-instance',
                     'user': 'airflowproxy', 'zone': 'europe-west1',
                     'database': 'airflow',
                     'password': 'secret'}, 'apiVersion': 'v1',
            'metadata': {'namespace': 'default',
                         'name': 'airflow-db'}}


def load_settings():
    with open('settings.yaml', 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def execute_with_yaml(template, command, apply_changes):
    with open(template, 'r') as stream:
        try:
            service = yaml.load(stream)
            apply_changes(service)
            p = Popen(command,
                      stdout=PIPE,
                      stdin=PIPE, stderr=PIPE)
            out, err = p.communicate(input=yaml.dump(service))
            print(out)
            print(err)

        except yaml.YAMLError as exc:
            print(exc)


def kubectl_patch(stage, name, image, version):
    path = [
        {"op": "replace", "path": "/metadata/labels/version",
         "value": version},
        {"op": "replace", "path": "/spec/template/metadata/labels/version",
         "value": version},
        {"op": "replace", "path": "/spec/template/spec/containers/0/image",
         "value": image + ":" + version}
    ]

    p = Popen(
        ['kubectl', 'patch', 'deployment', name, '--namespace',
         stage, '--type', 'json', '-p=' + json.dumps(path)],
        stdout=PIPE,
        stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out)
    print(err)


def kubectl_delete(stage, type, name):
    p = Popen(
        ['kubectl', 'delete', type, name, '--namespace',
         stage],
        stdout=PIPE,
        stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out)
    print(err)


def deploy_dbinit(stage):
    def apply_changes(service):
        service['metadata']['namespace'] = stage

    execute_with_yaml('k8s/deploy-dbinit.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def deploy_db(stage):
    def apply_changes(service):
        service['metadata']['namespace'] = stage

    execute_with_yaml('k8s/deploy-db.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def deploy_db(stage):
    def apply_changes(service):
        service['metadata']['namespace'] = stage

    execute_with_yaml('k8s/deploy-db.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def deploy_redis(stage):
    def apply_changes(service):
        service['metadata']['namespace'] = stage

    execute_with_yaml('k8s/deploy-redis.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def deploy_webserver(stage, version):
    def apply_changes(service):
        service['metadata']['namespace'] = stage
        service['metadata']['labels']['version'] = version
        service['spec']['template']['metadata']['labels']['version'] = version
        service['spec']['template']['spec']['containers'][0][
            'image'] = 'b.gcr.io/airflow-gcp/airflow-master:' + version

    execute_with_yaml('k8s/deploy-webserver.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def deploy_scheduler(stage, version):
    def apply_changes(service):
        service['metadata']['namespace'] = stage
        service['metadata']['labels']['version'] = version
        service['spec']['template']['metadata']['labels']['version'] = version
        service['spec']['template']['spec']['containers'][0][
            'image'] = 'b.gcr.io/airflow-gcp/airflow-master:' + version

    execute_with_yaml('k8s/deploy-scheduler.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def deploy_worker(stage, version):
    def apply_changes(service):
        service['metadata']['namespace'] = stage
        service['metadata']['labels']['version'] = version
        service['spec']['template']['metadata']['labels']['version'] = version
        service['spec']['template']['spec']['containers'][0][
            'image'] = 'b.gcr.io/airflow-gcp/airflow-worker:' + version

    execute_with_yaml('k8s/deploy-worker.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def service_webserver(stage):
    def apply_changes(service):
        service['metadata']['namespace'] = stage

    execute_with_yaml('k8s/service-webserver.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def service_db(stage):
    def apply_changes(service):
        service['metadata']['namespace'] = stage

    execute_with_yaml('k8s/service-db.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def service_redis(stage):
    def apply_changes(service):
        service['metadata']['namespace'] = stage

    execute_with_yaml('k8s/service-redis.yaml',
                      ['kubectl', 'create', '--namespace', stage, '-f', '-'],
                      apply_changes)


def gcloud():
    p = Popen(
        ['gcloud', 'config', 'list'],
        stdout=PIPE,
        stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(out))
    return config


def config():
    p = Popen(
        ['kubectl', 'get', '--namespace', 'default', 'configmap/airflow-db', '-o',
         'yaml'],
        stdout=PIPE,
        stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return yaml.load(out)


def create_airflow_config(stage):
    p = Popen(
        ['kubectl', 'create', 'configmap', 'airflow-config', '--namespace',
         stage, '--from-file', 'airflow.cfg=airflow-' + stage + '.cfg'],
        stdout=PIPE,
        stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out)
    print(err)


def get_environment_from(settings, environent):
    for env in settings['environments']:
        if env['name'] == environent:
            return env
    return None


def kubectl_airflow_config_settings(command, settings, environment):
    service = {
        'apiVersion': 'v1', 'kind': 'ConfigMap', 'data': {

        },
        'metadata': {
            'name': 'airflow-settings',
            'namespace': environment['namespace']
        }
    }

    service['data']['git-branch'] = environment['git']['branch']
    service['data']['git-repo-dag'] = environment['git']['repo-dag']
    service['data']['git-repo-plugin'] = environment['git']['repo-plugin']
    service['data']['staging-bucket'] = environment['staging-bucket']

    service['data']['sql-project'] = environment['database']['project']
    service['data']['sql-zone'] = environment['database']['zone']
    service['data']['sql-instance'] = environment['database']['instance']
    service['data']['sql-database'] = environment['database']['database']
    service['data']['sql-user'] = environment['database']['user']
    service['data']['sql-password'] = environment['database']['password']

    try:
        p = Popen(
            ['kubectl', command, '--namespace', environment['namespace'], '-f', '-'],
            stdout=PIPE,
            stdin=PIPE, stderr=PIPE)
        out, err = p.communicate(input=yaml.dump(service))
        print(out)
        print(err)

    except yaml.YAMLError as exc:
        print(exc)


def create_service_account(stage, key_file):
    p = Popen(
        ['kubectl', 'create', 'secret', 'generic', 'service-account', '--namespace',
         stage, '--from-file', "service-account.json=" + key_file],
        stdout=PIPE,
        stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out)
    print(err)


def create_proxy(stage):
    with open('k8s/deploy-redis.yaml', 'r') as stream:
        try:
            service = yaml.load(stream)
            service['metadata']['namespace'] = stage
            p = Popen(['kubectl', 'create', '--namespace', 'dev', '-f', '-'],
                      stdout=PIPE,
                      stdin=PIPE, stderr=PIPE)
            out, err = p.communicate(input=yaml.dump(service))
            print(out)
            print(err)

        except yaml.YAMLError as exc:
            print(exc)


print "Airflow for Google Cloud"
print
environment = None
while environment is None:
    print "Please select on of the environments to setup:"
    settings = load_settings()
    for env in settings['environments']:
        print '- ' + env['name']
    environment_name = raw_input("Environment: ")
    environment = get_environment_from(settings, environment_name)
namespace = environment['namespace']

version = '1.8.0.alpha.6'
print
print "1) Setup a new Airflow (version: " + version + ")"
print "2) Upgrade Airflow (version: " + version + ")"
print "9) Delete Airflow"
print "0) Help"

what = raw_input("Enter your choose: ")

if what == '0':
    print "Install/Upgrade Airflow for Google Cloud on a GKE cluster"
elif what == '1':

    kubectl_airflow_config_settings('create', settings, environment)
    create_service_account(namespace, environment['service-accounts'][0]['path'])
    create_airflow_config(namespace)

    service_webserver(namespace)
    service_redis(namespace)
    service_db(namespace)

    deploy_db(namespace)
    deploy_redis(namespace)
    deploy_scheduler(namespace, version)
    deploy_worker(namespace, version)
    deploy_webserver(namespace, version)
elif what == '2':

    kubectl_airflow_config_settings('apply', 'development', settings)
    kubectl_patch(namespace, "airflow-webserver",
                  "b.gcr.io/airflow-gcp/airflow-master",
                  version)
    kubectl_patch(namespace, "airflow-scheduler",
                  "b.gcr.io/airflow-gcp/airflow-master",
                  version)
    kubectl_patch(namespace, "airflow-worker", "b.gcr.io/airflow-gcp/airflow-worker",
                  version)
elif what == '9':
    kubectl_delete(namespace, "deployment", "airflow-webserver")
    kubectl_delete(namespace, "deployment", "airflow-worker")
    kubectl_delete(namespace, "deployment", "airflow-scheduler")
    kubectl_delete(namespace, "deployment", "airflow-dbinit")
    kubectl_delete(namespace, "deployment", "airflow-settings")
    kubectl_delete(namespace, "deployment", "airflow-db")
    kubectl_delete(namespace, "deployment", "airflow-redis")
    kubectl_delete(namespace, "services", "airflow-redis")
    kubectl_delete(namespace, "services", "airflow-db")
    # kubectl_delete(current_stage, "services", "airflow")
    kubectl_delete(namespace, "configmap", "airflow-settings")
    kubectl_delete(namespace, "configmap", "airflow-config")
    kubectl_delete(namespace, "secrets", "service-account")
else:
    print "Nothing todo, exiting"
