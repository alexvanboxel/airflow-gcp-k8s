import ConfigParser
import io
import json
import sys
import tempfile
from subprocess import PIPE, Popen
from time import sleep

import yaml


def load_settings():
    with open('settings.yaml', 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def load_versions_public():
    with open('versions_public.yaml', 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def load_versions_private():
    try:
        with open('versions_private.yaml', 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    except IOError:
        return None


def output_stdout(out, err):
    if len(out) > 0:
        print(out)
    if len(err) > 0:
        print(err)


def execute_with_yaml(template, command, apply_changes=None):
    with open(template, 'r') as stream:
        try:
            service = yaml.load(stream)
            if apply_changes is not None:
                apply_changes(service)
            p = Popen(command,
                      stdout=PIPE,
                      stdin=PIPE, stderr=PIPE)
            out, err = p.communicate(input=yaml.dump(service))
            output_stdout(out, err)

        except yaml.YAMLError as exc:
            print(exc)


def execute_process(command):
    p = Popen(command,
              stdout=PIPE,
              stdin=PIPE, stderr=PIPE)
    out, err = p.communicate()
    output_stdout(out, err)


def kubectl_patch(name, image, version):
    path = [
        {"op": "replace", "path": "/metadata/labels/version",
         "value": version},
        {"op": "replace", "path": "/spec/template/metadata/labels/version",
         "value": version},
        {"op": "replace", "path": "/spec/template/spec/containers/0/image",
         "value": image + ":" + version}
    ]

    execute_process(
        ['kubectl', 'patch', 'deployment', name, '--namespace',
         namespace, '--type', 'json', '-p=' + json.dumps(path)])


def kubectl_delete(type, name):
    execute_process(
        ['kubectl', 'delete', type, name, '--namespace',
         namespace])


def deploy_db():
    execute_with_yaml('k8s/airflow-db-deploy.yaml',
                      ['kubectl', 'create', '--namespace', namespace, '-f', '-'])


def deploy_redis():
    execute_with_yaml('k8s/airflow-redis-deploy.yaml',
                      ['kubectl', 'create', '--namespace', namespace, '-f', '-'])


def deploy_sync():
    execute_with_yaml('k8s/airflow-sync-deploy.yaml',
                      ['kubectl', 'create', '--namespace', namespace, '-f', '-'])
    sleep(30)


def deploy_airflow(name, image_suffix):
    def apply_changes(service):
        service['metadata']['labels']['version'] = version
        service['spec']['template']['metadata']['labels']['version'] = version
        service['spec']['template']['spec']['containers'][0][
            'image'] = repo + '/airflow-' + image_suffix + ':' + version

    execute_with_yaml('k8s/airflow-' + name + '-deploy.yaml',
                      ['kubectl', 'create', '--namespace', namespace, '-f', '-'],
                      ,)


def deploy_upgradedb():
    def apply_changes(service):
        service['metadata']['name'] = "airflow-upgrade-" + version
        service['metadata']['namespace'] = namespace
        service['spec']['template']['spec']['containers'][0][
            'image'] = repo + '/airflow-master:' + version

    execute_with_yaml('k8s/job-upgradedb.yaml',
                      ['kubectl', 'create', '--namespace', namespace, '-f', '-'],
                      apply_changes)


def deploy_initdb():
    def apply_changes(service):
        service['metadata']['name'] = "airflow-initdb-" + version
        service['metadata']['namespace'] = namespace
        service['spec']['template']['spec']['containers'][0][
            'image'] = repo + '/airflow-master:' + version

    execute_with_yaml('k8s/job-initdb.yaml',
                      ['kubectl', 'create', '--namespace', namespace, '-f', '-'],
                      apply_changes)


def service(service_name):
    def apply_changes(service):
        service['metadata']['namespace'] = namespace

    execute_with_yaml('k8s/service-' + service_name + '.yaml',
                      ['kubectl', 'create', '--namespace', namespace, '-f', '-'],
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


def create_airflow_config():
    config = ConfigParser.ConfigParser()
    config.readfp(open('airflow-template.cfg'))

    config.set('core', 'remote_log_conn_id', environment['logging']['conn_id'])
    config.set('core', 'remote_base_log_folder', environment['logging']['bucket'])
    config.set('webserver', 'base_url', environment['webserver']['base_url'])
    config.set('webserver', 'web_server_port', 8080)

    config.set('google', 'client_id', settings['auth']['client_id'])
    config.set('google', 'client_secret', settings['auth']['client_secret'])
    config.set('google', 'domain', settings['auth']['domain'])
    tmp = tempfile.NamedTemporaryFile()
    config.write(tmp)
    tmp.flush()
    execute_process(
        ['kubectl', 'create', 'configmap', 'airflow-config', '--namespace',
         namespace, '--from-file', 'airflow.cfg=' + tmp.name])


def get_environment_from():
    for env in settings['environments']:
        if env['name'] == environment_name:
            return env
    return None


def kubectl_airflow_config_settings(command):
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

    service['data']['sql-project'] = settings['database-init']['proxy']['project']
    service['data']['sql-zone'] = settings['database-init']['proxy']['zone']
    service['data']['sql-instance'] = settings['database-init']['proxy']['instance']
    service['data']['sql-database'] = environment['database']['database']
    service['data']['sql-user'] = environment['database']['user']
    service['data']['sql-password'] = environment['database']['password']
    service['data']['sql-root-user'] = settings['database-init']['user']
    service['data']['sql-root-password'] = settings['database-init']['password']

    try:
        p = Popen(
            ['kubectl', command, '--namespace', environment['namespace'], '-f', '-'],
            stdout=PIPE,
            stdin=PIPE, stderr=PIPE)
        out, err = p.communicate(input=yaml.dump(service))
        output_stdout(out, err)

    except yaml.YAMLError as exc:
        print(exc)


def kubectl(command, k8s_file):
    def apply_changes(service):
        service['metadata']['namespace'] = namespace

    execute_with_yaml(k8s_file,
                      ['kubectl', command, '--namespace', namespace, '-f', '-'],
                      apply_changes)


def kubectl_create_namespace():
    execute_process(
        ['kubectl', 'create', 'namespace', namespace])


def create_service_account(key_file):
    execute_process(
        ['kubectl', 'create', 'secret', 'generic', 'service-account', '--namespace',
         namespace, '--from-file', "service-account.json=" + key_file])



print "Airflow for Google Cloud"
print
environment = None
settings = load_settings()
version_public = load_versions_public()
version_private = load_versions_private()

print str(version_public)
print str(version_private)
if version_private is None:
    repo = 'b.gcr.io/airflow-gcp'
    version = version_public['public']['version']
    print "Using public repo"
    print repo + ":" + version
else:
    repo = version_private['private']['repo']
    version = version_private['private']['version']
    print "Using private repo"
    print repo + ":" + version

while environment is None:
    print "Please select on of the environments to setup:"
    for env in settings['environments']:
        print '- ' + env['name']
    environment_name = raw_input("Environment: ")
    environment = get_environment_from()
namespace = environment['namespace']

print
print "Make sure you met the pre-requirement and pre-setup. Consult the README file."
print "This setup procedure is not really forgiving."
print
print "1) Setup a new Airflow (version: " + version + ")"
print "2) Upgrade Airflow (version: " + version + ")"
print "9) Delete Airflow"
print "0) Help"

what = raw_input("Enter your choose: ")

if what == '0':
    print "Install/Upgrade Airflow for Google Cloud on a GKE cluster"
elif what == '1':
    kubectl_create_namespace()
    kubectl_airflow_config_settings('create')
    create_service_account(environment['service-accounts'][0]['path'])
    create_airflow_config()

    service('webserver')
    service('redis')
    service('db')

    deploy_redis()
    deploy_db()
    deploy_sync()

    what = raw_input("Do you want to create a database (Y to create)? ")
    if what == 'Y':
        deploy_initdb()
        what = raw_input("ENTER if database is created. ")

    deploy_airflow('worker', 'worker')
    deploy_airflow('webserver', 'master')
    deploy_airflow('scheduler', 'master')
elif what == '2':
    kubectl_airflow_config_settings('apply')

    what = raw_input("Do you want to upgrade the database (Y to create)? ")
    if what == 'Y':
        deploy_upgradedb()
        what = raw_input("ENTER if database is created. ")

    kubectl_patch("airflow-webserver",
                  repo + "/airflow-master",
                  version)
    kubectl_patch("airflow-scheduler",
                  repo + "/airflow-master",
                  version)
    kubectl_patch("airflow-worker", repo + "/airflow-worker",
                  version)
elif what == '9':
    kubectl_delete("deployment", "airflow-webserver")
    kubectl_delete("deployment", "airflow-worker")
    kubectl_delete("deployment", "airflow-scheduler")
    kubectl_delete("deployment", "airflow-db")
    kubectl_delete("deployment", "airflow-redis")
    kubectl_delete("deployment", "airflow-sync")
    kubectl_delete("services", "airflow-redis")
    kubectl_delete("services", "airflow-db")
    #kubectl_delete("services", "airflow")
    kubectl_delete("configmap", "airflow-settings")
    kubectl_delete("configmap", "airflow-config")
    kubectl_delete("secrets", "service-account")
else:
    print "Nothing todo, exiting"
