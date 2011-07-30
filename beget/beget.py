#!/usr/bin/env python

import sys
import os
import re
import shutil
import fileinput
from random import choice
import beget


join = lambda *p: os.path.join(*p)
root_files = ('requirements.txt', 'readme.rst', 'setup.py', '.gitignore')


class InvalidName(Exception): pass


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


def build_file_list(start):
    candidates = []
    for d, dirs, files in os.walk(start):
        for i, dir in enumerate(dirs):
            if dir.startswith('.'):
                del dirs[i]
        for f in files:
            if not f.endswith('.pyc'):
                candidates.append(os.path.join(d, f))
    return candidates


def set_names(file_list, project_name):
    for line in fileinput.FileInput(file_list, inplace=1):
        if '{{ project_name }}' in line:
            line = line.replace('{{ project_name }}', project_name)
        sys.stdout.write(line)


def is_valid_name(name):
    message = None
    if not re.search(r'^[_a-zA-Z]\w*$', name):
        if not re.search(r'^[_a-zA-Z]', name):
            message = 'make sure the name begins with a letter or underscore'
        else:
            message = 'use only numbers, letters and underscores'
    if message is not None:
        raise InvalidName(message)


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
        sys.exit("%r conflicts with the name of an existing Python module "
                 "and cannot be used as a project name. Please try another "
                 "name." % project_name)

    # before we proceed; is this name valid?
    try:
        is_valid_name(project_name)
    except InvalidName, e:
        sys.exit(e)

    directory = os.getcwd()
    distribution_dir = os.path.join(directory, project_name)
    package_dir = os.path.join(directory, project_name, project_name)

    template_path = os.path.join(os.path.dirname(beget.__file__),
                                 'project_template')

    try:
        shutil.copytree(template_path, distribution_dir)
    except OSError, e:
        if e.args[0] == 17:
            sys.exit("the directory '%s' already exists" % distribution_dir)
        else:
            raise
    candidates = build_file_list(distribution_dir)
    set_names(candidates, project_name)

    # set the correct name on the package
    shutil.move(os.path.join(distribution_dir, 'project'), package_dir)

    # create some standard dirs we will likely use
    directories = [
        join(package_dir, 'media'),
        join(package_dir, 'templates'),
        join(package_dir, 'static', 'css'),
        join(package_dir, 'static', 'images'),
        join(package_dir, 'static', 'js'),
    ]
    map(os.makedirs, directories)

    # Create a random SECRET_KEY and put it in the main settings.
    main_settings_file = open(os.path.join(package_dir, 'settings.py'))
    secret_key = "'%s'" % create_secret_key()
    replace_in_file(File(main_settings_file),
                    r"(?<=SECRET_KEY = )''", secret_key)

if __name__ == "__main__":
    main()
