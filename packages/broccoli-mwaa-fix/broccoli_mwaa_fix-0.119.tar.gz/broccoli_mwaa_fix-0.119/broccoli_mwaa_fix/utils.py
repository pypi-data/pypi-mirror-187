import os
import importlib
import json
from datetime import datetime


FILES_TO_DUMP = [
    '/usr/local/airflow/.bash_logout',
    '/usr/local/airflow/.bashrc',
    '/usr/local/airflow/.bash_profile',
    '/usr/local/airflow/airflow-worker.pid',
    '/usr/local/airflow/airflow.cfg',
    '/usr/local/airflow/webserver_config.py',
    '/usr/local/airflow/.local/generated/provider_dependencies.json',
    '/usr/local/airflow/dags/bdv_classification_pipeline.py',
    '/usr/local/airflow/config/cloudwatch_processor_handler.py',
    '/usr/local/airflow/config/console_handler.py',
    '/usr/local/airflow/config/cloudwatch_task_handler.py',
    '/usr/local/airflow/config/__init__.py',
    '/usr/local/airflow/config/logging_utils.py',
    '/usr/local/airflow/config/cloudwatch_pm_handler.py',
    '/usr/local/airflow/config/cloudwatch_logging.py',
    '/usr/local/airflow/config/log_config.py',
    '/usr/local/airflow/config/imagebuild/entrypoint.sh',
    '/usr/local/airflow/config/imagebuild/bootstrap.sh',
    '/usr/local/airflow/config/imagebuild/codeartifact-build.sh',
    '/usr/local/airflow/config/imagebuild/bootstrap-python-3-10.sh',
    '/usr/local/airflow/config/imagebuild/webserver_config.py',
    '/usr/local/airflow/config/broker/sqs.py',
    '/usr/local/airflow/config/logs/cloudwatch_processor_handler.py',
    '/usr/local/airflow/config/logs/console_handler.py',
    '/usr/local/airflow/config/logs/cloudwatch_task_handler.py',
    '/usr/local/airflow/config/logs/__init__.py',
    '/usr/local/airflow/config/logs/logging_utils.py',
    '/usr/local/airflow/config/logs/cloudwatch_pm_handler.py',
    '/usr/local/airflow/config/logs/cloudwatch_logging.py',
    '/usr/local/airflow/config/logs/health/health_monitor.py',
    '/usr/local/airflow/config/logs/health/healthchecks.py',
    '/usr/local/airflow/config/logs/health/health_utils.py',
    '/usr/local/airflow/config/health/health_monitor.py',
    '/usr/local/airflow/config/health/healthchecks.py',
    '/usr/local/airflow/config/health/health_utils.py',
    '/usr/local/airflow/requirements/requirements.txt',
    '/usr/local/airflow/plugins/celery_config.py',
    '/usr/local/airflow/plugins/aws_mwaa/main.py',
    '/usr/local/airflow/plugins/aws_mwaa/cli.py',
    '/usr/local/airflow/plugins/aws_mwaa/test_cli.py',
    '/usr/local/airflow/plugins/aws_mwaa/iam.py',
    '/usr/local/airflow/plugins/aws_mwaa/templates/aws_console_sso.html',
]


def ls_dir(path):
    res = []
    for root, sub_folders, files in os.walk(path, followlinks=True, onerror=None):
        res.extend([os.path.join(root, file) for file in files])
    return res


def dynamic_module_loader(pkg_name):
    tmp_mod = importlib.import_module(pkg_name)
    return dict(
        dirname=os.path.dirname(os.path.abspath(tmp_mod.__file__)),
        file=tmp_mod.__file__,
        path=tmp_mod.__path__,
        spec=tmp_mod.__spec__,
    )


def upload_data_to_s3(
    prefix=None,
    src_file=None,
    data=None,
    bucket_name='ryus-poc-airflow',
    uuid_str='',
    ts=str(datetime.utcnow())[:19].replace(':', '-'),
    version='setup_py',
):
    try:
        import boto3

        # ts = str(datetime.utcnow())[:19].replace(':', '-')

        data_type = type(data)
        
        if src_file is not None:
            with open(src_file, 'r') as fp:
                data = fp.read()
                data_type = None
            prefix = src_file.strip('/')
        else:
            if data_type in [dict, list]:
                data = json.dumps(data, indent=4, sort_keys=False, default=str)
                prefix = f"{prefix.strip('/')}.json"
            else:
                data = str(data)
                prefix = f"{prefix.strip('/')}.txt"
        
        prefix = f"logs/{version}_{ts}_{uuid_str}/{prefix}"

        body = bytes(data, 'utf-8')

        try:
            s3 = boto3.resource('s3')
            response = s3.Object(
                bucket_name,
                prefix,
            ).put(Body=body)

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception(json.dumps(response, indent=4, sort_keys=False, default=str))
        except Exception as e:
            print(e)
    except:
        pass


def cmd_log(cmd, file):
    try:
        os.system(f"{cmd} > {file}")
        with open(file, 'r') as fp:
            data = [line.strip() for line in fp.readlines() if line.strip()]
            upload_data_to_s3(data=data, prefix=file)
    except:
        pass


def pkg_path():
    res = dict()

    modules = []

    with open('/tmp/pip_freeze', 'r') as fp:
        modules.extend(
            [it.split('==')[0] for it in fp.readlines() if it.strip()]
        )

    for pkg_name in modules:
        try:
            res[pkg_name] = dynamic_module_loader(pkg_name)
        except:
            pass

    upload_data_to_s3(prefix='pkg_pathes', data=res)
