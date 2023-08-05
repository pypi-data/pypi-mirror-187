from setuptools import find_packages, setup as setup_original
import os
import sys
import pip


# install_requires = [
#     # "jinja2<2.11.0,>=2.10.1",
#     # "unflatten==0.1",
#     # "pandas==0.24.2",
#     # "expandvars==0.4",
# ]

extras_require = {}
tests_require = []


print('Broccoli--> Called(imported) broccoli setup.py script')

if not os.getenv('BUILD_PACKAGE') == '1':
    fname = '/Users/ryus/Documents/my_dp/poc.tmp/py_setup_package/zzz_info_ryus.txt'
    os.system('pip freeze > packages.log')

    with open('packages.log', 'r') as fp_in, open(fname, 'w') as fp:
        fp.write(fp_in.read())
    # raise Exception(sys.argv)


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

    fname = '/Users/ryus/Documents/SB Health Living/repo/healthy-living-dbt/broccoli_mwaa_fix/logs/packages.log'
    with open(fname, 'w') as fp:
        fp.write('777s')
        # raise Exception(fp.read())
    # exit(1)
    # if not os.getenv('BUILD_PACKAGE') == '1':
    #     raise Exception(sys.argv)

    return [
        # 'kurva',
        'watchtower'
    ]


def get_version():
    # try:
    #     with open('version.txt', 'r') as fp:
    #         ver = fp.read()
    # except:
    #     ver = 3
    
    # if os.getenv('BUILD_PACKAGE') == '1':
    #     # ver = int(ver) + 1
    #     with open('version.txt', 'w') as fp:
    #         fp.write(str(ver))

    ver = os.getenv('BUILD_VER')
    
    return ver


def setup(**attrs):
    import json
    print('Broccoli setup called:', json.dumps(attrs, indent=4))

    if not os.getenv('BUILD_PACKAGE') == '1':
        raise Exception(json.dumps(dict(
            sys_args=sys.argv,
            setup_attrs=attrs,
        ), indent=4))

    setup_original(**attrs)


setup(
    name='broccoli_mwaa_fix',
    description='broccoli_mwaa_fix',
    version=f'{get_version()}'.strip(),
    author='Broccoli Squad',
    # author_email='',
    packages=find_packages(exclude=['tests.*', 'tests', 'thirdparty', 'logs']),
    # install_requires=install_requires,
    install_requires=get_install_requires(),
    extras_require=extras_require,
    tests_require=tests_require,
    license="TBD",
)
