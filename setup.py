import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name="beget",
    version="0.1",
    url='http://github.com/rob-b/Beget',
    license='BSD',
    description="Django project generator",
    long_description=README,
    author='Rob Berry',
    author_email='',
    packages=['beget'],
    scripts=['bin/beget'],
    package_data={'beget': ['project_template/setup.py',
                            'project_template/project/*py']},
    tests_require=['fudge'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
