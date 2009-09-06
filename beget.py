#!/usr/bin/env python

from django.core import management
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

def main():

    # we shift around the argv and then call the default django startproject
    # command.
    try:
        sys.argv.append(sys.argv[1])
    except IndexError:
        sys.exit('Project name required')
    sys.argv[1] = 'startproject'
    management.execute_from_command_line()

    directory, project_name = os.getcwd(), sys.argv[2]
    project_path = os.path.join(directory, project_name)

    # create some standard dirs we will likely use
    os.mkdir(os.path.join(project_path, 'templates'))
    for dir in ('css', 'img', 'js'):
        os.makedirs(os.path.join(project_path, 'assets', dir))

    # copy over our settings
    update_settings(project_path, project_name)

    # Create a random SECRET_KEY hash, and put it in the main settings.
    main_settings_file = os.path.join(directory, project_name, 'settings.py')
    settings_contents = open(main_settings_file, 'r').read()
    fp = open(main_settings_file, 'w')
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    settings_contents = re.sub(r"(?<=SECRET_KEY = ')'", secret_key + "'", settings_contents)
    fp.write(settings_contents)
    fp.close()

if __name__ == "__main__":
    main()
