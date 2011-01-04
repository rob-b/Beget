from setuptools import setup

setup(
    name = "beget",
    version = "0.1",
    url = 'http://github.com/rob-b/Beget',
    license = 'BSD',
    description = "Django project generator",
    author = 'rob-b',
    packages = ['beget'],
    scripts=['bin/beget'],
    install_requires = ['setuptools'],
    package_data={'': ['project_template/*py']},
)
