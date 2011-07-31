#!/usr/bin/env python

import sys
import os
import re
import shutil
import fileinput
from random import choice
from optparse import OptionParser
import beget


parser = OptionParser(usage="usage: %prog [options] projectname")
parser.add_option("-k", "--like-krak3n", action="store_true",
                  dest='settings_package')


class InvalidName(Exception): pass


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


def set_names(file_list, project_name, needle='{{ project_name }}' ):
    for line in fileinput.FileInput(file_list, inplace=1):
        if needle in line:
            line = line.replace(needle, project_name)
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
    set_names([fobj.name], replacement, st)


def validate_args(parser):
    options, args = parser.parse_args()
    try:
        project_name = args[0]
    except IndexError:
        parser.error('Project name required')
    if len(args) > 1:
        parser.error('Too many arguments')
    return options, args


def main():
    options, args = validate_args(parser)
    project_name = args[0]

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
        os.path.join(package_dir, 'media'),
        os.path.join(package_dir, 'templates'),
        os.path.join(package_dir, 'static', 'css'),
        os.path.join(package_dir, 'static', 'images'),
        os.path.join(package_dir, 'static', 'js'),
    ]
    map(os.makedirs, directories)

    # Create a random SECRET_KEY and put it in the main settings.
    secret_key = "SECRET_KEY = '%s'" % create_secret_key()
    settings_file = os.path.join(package_dir, 'settings.py')
    with open(settings_file) as settings:
        replace_in_file(settings, "SECRET_KEY = ''", secret_key)

    if options.settings_package:
        config_dir = os.path.join(package_dir, 'config')
        os.makedirs(config_dir)
        common = os.path.join(config_dir, 'common.py')
        shutil.move(settings_file, common)
        with open(os.path.join(config_dir, '__init__.py'), 'w') as a:
            a.write('')

        with open(common) as common:
            replace_in_file(common,
                            'PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))',
                            "PROJECT_ROOT = os.path.dirname(os.path.realpath(os.path.join(__file__, '..')))")


if __name__ == "__main__":
    main()
