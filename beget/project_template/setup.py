"""based on django's setup.py"""
import os
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES


# make distutils install our data files alongisde our .py files
for scheme in INSTALL_SCHEMES.values():
        scheme['data'] = scheme['purelib']


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
extensions_dir = '{{ project_name }}'


for d, dirs, files in os.walk(extensions_dir):
    for i, dirname in enumerate(dirs):
        if dirname.startswith('.'):
            del dirs[i]
    if '__init__.py' in files:
        packages.append('.'.join(fullsplit(d)))
    elif files:
        data_files.append([d, [os.path.join(d, f) for f in files]])


setup(
    name="{{ project_name }}",
    version="0.1.0",
    zip_safe=False,
    packages=packages,
    data_files=data_files,
)
