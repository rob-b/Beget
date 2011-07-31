=====
Beget
=====

Beget is a very simple tool to create a default django project. It basically does little more than ``django-admin.py startproject projectname`` with the only differences being that it creates the project in a python distribution layout complete with setup.py for ease of installation and creates media and static directories.

The default settings.py is tailored to the author's preferences i.e. TIME_ZONE is set to 'Europe/London'.

Usage
-----

To use beget::

    > beget example_project

This will create the following directories::

    > tree example_project
    example_project
    ├── example_project
    │   ├── __init__.py
    │   ├── media
    │   ├── settings.py
    │   ├── static
    │   │   ├── css
    │   │   ├── images
    │   │   └── js
    │   ├── templates
    │   └── urls.py
    └── setup.py

beget has only one option (excluding ``--help`` of course)::

    > beget -h
    Usage: beget [options] projectname

    Options:
      -h, --help         show this help message and exit
      -k, --like-krak3n  Create config/common.py instead of settings.py

The ``-k`` or ``--like-krak3n`` option replaces settings.py with config/common.py as is the way of the krak3n::

    > beget --like-krak3n example_project && tree example_project
    example_project
    ├── example_project
    │   ├── config
    │   │   ├── common.py
    │   │   └── __init__.py
    │   ├── __init__.py
    │   ├── media
    │   ├── static
    │   │   ├── css
    │   │   ├── images
    │   │   └── js
    │   ├── templates
    │   └── urls.py
    └── setup.py
