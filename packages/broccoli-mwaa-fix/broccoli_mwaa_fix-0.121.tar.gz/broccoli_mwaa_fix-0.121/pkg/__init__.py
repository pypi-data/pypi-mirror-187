import os


def get_version():
    # fname = f"{os.path.dirname(os.path.abspath(__file__))}/pkg/version.py"
    fname = f"{os.path.dirname(os.path.abspath(__file__))}/version.py"
    with open(fname, 'r') as fp:
        ver = fp.read().strip()

    if os.getenv('BUILD_PACKAGE') == '1':
        ver = int(ver) + 1
        
        with open(fname, 'w') as fp:
            fp.write(str(ver))
    
    return ver
