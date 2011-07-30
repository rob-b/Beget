import os
from setuptools import setup
from setuptools import find_packages


data_files = []
package_data = []
for d, dirs, files in os.walk('throwaway'):
    for i, dirname in enumerate(dirs):
        if dirname.startswith('.'):
            del dirs[i]
        if files and '__init__.py' not in files:
            data_files.append([d, [os.path.join(d, f) for f in files]])
            package_data.append([os.path.join(d, f) for f in files])


setup(
    name="{{ project_name }}",
    version="0.1.0",
    zip_safe=False,
    packages=find_packages(),
    data_files=data_files,
    package_data={"{{ project_name }}": package_data},
)
