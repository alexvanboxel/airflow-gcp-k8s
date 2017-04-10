import subprocess
import os
import logging
import sys
import git
from subprocess import Popen, PIPE, STDOUT


def cmd(args):
    process = Popen(args, stdout=PIPE, stderr=STDOUT, shell=True)
    with process.stdout:
        log_subprocess_output(process.stdout)


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        logging.debug(line.strip())


def check_env_vars():
    to_check = ['SYNC_REPO_DAG', 'SYNC_REPO_PLUGIN', 'SYNC_STAGING_BUCKET', 'SYNC_BRANCH']

    not_set = []
    for var in to_check:
        if var not in os.environ:
            not_set.append(var)
    if not_set:
        print("Env vars not set: %s", vars)
        raise Exception


def git_changes(repo, prev_head):
    diffs = repo.tree(prev_head).diff('HEAD')

    changed_files = []
    for x in diffs:
        if x.a_blob is not None and x.a_blob.path not in changed_files:
            changed_files.append(x.a_blob.path)

        if x.b_blob is not None and x.b_blob.path not in changed_files:
            changed_files.append(x.b_blob.path)

    return changed_files


def git_log(repo, prev_head):
    r = git.Repo(repo)
    if r.head.object.hexsha == prev_head:
        return []

    git_commit_fields = ['id', 'author_name', 'author_email', 'date', 'message']
    git_log_format = ['%H', '%an', '%ae', '%ad', '%s']
    git_log_format = '%x1f'.join(git_log_format) + '%x1e'

    p = Popen('cd %s && git log %s..HEAD --format="%s"' % (repo, prev_head, git_log_format), shell=True, stdout=PIPE)
    (log, _) = p.communicate()
    log = log.strip('\n\x1e').split("\x1e")
    log = [row.strip().split("\x1f") for row in log]
    log = [dict(zip(git_commit_fields, row)) for row in log]

    return log


def clone_repo():
    check_env_vars()

    cmd('mkdir -p /home/airflow/logs')
    cmd('mkdir -p /home/airflow/staging')

    cmd('gcloud source repos clone $SYNC_REPO_DAG /home/airflow/dags')
    cmd('cd /home/airflow/dags && git checkout $SYNC_BRANCH')

    cmd('gcloud source repos clone $SYNC_REPO_PLUGIN /home/airflow/plugins')
    cmd('cd /home/airflow/plugins && git checkout $SYNC_BRANCH')

    logging.info('Cloning done.')


def sync():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    cmd('gcloud auth activate-service-account --key-file /secret/service-account.json')

    dags = None
    plugins = None
    dags_prev_head = None
    plugins_prev_head = None
    dag_changes = None
    plugin_changes = None
    dags_log = None
    pull = False
    # check if airflow home mounted
    if not os.path.isdir('/home/airflow'):
        logging.error('Airflow home not mounted')
        raise Exception
    if not os.path.isdir('/home/airflow/dags'):
        logging.error('No dags repo found, cloning from cloud...')
        clone_repo()
    else:
        pull = True
        # store git head sha
        dags = git.Repo("/home/airflow/dags")
        plugins = git.Repo("/home/airflow/plugins")
        dags_prev_head = dags.head.object.hexsha
        plugins_prev_head = plugins.head.object.hexsha

        # pull changes from repo
        logging.info('Pulling changes from repo')
        cmd('cd /home/airflow/dags && git pull')
        logging.info('Dags pull done')
        cmd('cd /home/airflow/plugins && git pull')
        logging.info('Dags pull done')

        dag_changes = git_changes(dags, dags_prev_head)
        plugin_changes = git_changes(plugins, plugins_prev_head)
        dags_log = git_log('/home/airflow/dags', dags_prev_head)

    # sync staging folder
    cmd('gsutil rsync -r $SYNC_STAGING_BUCKET /home/airflow/staging')
    logging.info("Synced staging folder")
    logging.info("All done.")

    if pull:
        return {'pull': True,
                'changes':
                    {'dags_old_head': dags_prev_head,
                     'dags_new_head': dags.head.object.hexsha,
                     'dag_changes': dag_changes,
                     'plugins_old_head': plugins_prev_head,
                     'plugins_new_head': plugins.head.object.hexsha,
                     'plugin_changes': plugin_changes
                     },
                'log': dags_log
                }
    return {'clone': True}




