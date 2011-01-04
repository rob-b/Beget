#!/usr/bin/env python

import sys
import os
import re
from random import choice
import beget


join = lambda *p: os.path.join(*p)
root_files = ('REQUIREMENTS.txt', 'README', 'setup.py', 'fabfile.py',
              '__init__.py')


class File(object):

    def __init__(self, file, name=None):
        self.file = file
        if name is None:
            name = getattr(self.file, 'name')
        self.name = name
        self.mode = getattr(self.file, 'mode')

    @classmethod
    def open_file(klass, path, mode='r'):
        self = klass(open(path, mode))
        return self

    def open(self, mode='r'):
        if not self.closed:
            self.file.seek(0)
        elif self.name and os.path.exists(self.name):
            self.file = open(self.name, mode or self.mode)

    def close(self):
        self.file.close()

    @property
    def closed(self):
        return not self.file or self.file.closed

    def read(self):
        return self.file.read()

    def write(self, s):
        return self.file.write(s)


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
            old_file = File.open_file(os.path.join(d, f), 'r')
            new_file = File.open_file(os.path.join(project_path, f), 'w')
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


def create_secret_key(length=50):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join([choice(chars) for i in range(length)])


def replace_in_file(fobj, st, replacement):
    content = fobj.read()
    content = re.sub(st, replacement, content)
    fobj.close()
    fobj.open('w')
    fobj.write(content)
    return content


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
        dest = join(project_parent, f)
        open(dest, 'w')

    # create some standard dirs we will likely use
    directories = [
        join(project_parent, 'media'),
        join(project_path, 'templates'),
        join(project_path, 'static', 'css'),
        join(project_path, 'static', 'images'),
        join(project_path, 'static', 'js'),
    ]
    map(os.makedirs, directories)

    # copy over our settings
    update_settings(project_path, project_name)

    # Create a random SECRET_KEY and put it in the main settings.
    main_settings_file = open(os.path.join(project_path, 'settings.py'))
    secret_key = "'%s'" % create_secret_key()
    replace_in_file(File(main_settings_file),
                    r"(?<=SECRET_KEY = )''", secret_key)

if __name__ == "__main__":
    main()
