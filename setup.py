from setuptools import setup


setup(
    name="beget",
    version="0.1",
    url='http://github.com/rob-b/Beget',
    license='BSD',
    description="Django project generator",
    author='Rob Berry',
    packages=['beget'],
    scripts=['bin/beget'],
    package_data={'beget': ['project_template/setup.py',
                            'project_template/project/*py']},
    tests_require=['fudge'],
    zip_safe=False,
)
