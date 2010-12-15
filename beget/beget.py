#!/usr/bin/env python

import sys
import os
import re
from random import choice
import beget

def update_settings(project_path, name):
    template_path = os.path.join(os.path.dirname(beget.__file__),
                                 'project_template')
    for d, dirs, files in os.walk(template_path):
        for i, dir in enumerate(dirs):
            if dir.startswith('.'):
                del dirs[i]
        for f in files:
            if f.endswith('.pyc'):
                continue
            old_file = open(os.path.join(d, f), 'r')
            new_file = open(os.path.join(project_path, f), 'w')
            new_file.write(old_file.read().replace('{{ project_name }}', name))
            new_file.close()
            old_file.close()


def is_valid_name(name):
    message = None
    if not re.search(r'^[_a-zA-Z]\w*$', name):
        # Provide a smart error message, depending on the error.
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
    return message

root_files = ('REQUIREMENTS.txt', 'README', 'setup.py', 'fabfile.py',
              '__init__.py')

def main():
    try:
        project_name = sys.argv[1]
    except IndexError:
        sys.exit('Project name required')

    # make sure that there is not already a module with this name
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        sys.exit("%r conflicts with the name of an existing Python module and "
                 "cannot be used as a project name. Please try another name." %
                 project_name)
    # before we proceed; is this name valid?
    message = is_valid_name(project_name)
    if message is not None:
        sys.exit(message)

    directory = os.getcwd()
    project_parent = os.path.join(directory, project_name)
    project_path = os.path.join(directory, project_name, project_name)


    # make the project directory
    try:
        os.makedirs(project_path)
    except OSError, e:
        if e.args[0] == 17:
            sys.exit("the directory '%s' already exists" % project_path)
        else:
            raise

    for f in root_files:
        dest = os.path.join(project_parent, f)
        open(dest, 'w')

    # create some standard dirs we will likely use
    os.mkdir(os.path.join(project_path, 'templates'))
    for di in ('css', 'img', 'js'):
        os.makedirs(os.path.join(project_path, 'assets', di))

    # copy over our settings
    update_settings(project_path, project_name)

    # Create a random SECRET_KEY hash, and put it in the main settings.
    main_settings_file = os.path.join(project_path, 'settings.py')
    settings_contents = open(main_settings_file, 'r').read()
    fp = open(main_settings_file, 'w')
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    settings_contents = re.sub(r"(?<=SECRET_KEY = ')'", secret_key + "'", settings_contents)
    fp.write(settings_contents)
    fp.close()

if __name__ == "__main__":
    main()
