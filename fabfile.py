#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import webbrowser

from fabric.api import local
from fabric.contrib import django


def test(module='tests'):
    """
    Runs all unit tests for OpenSlides using coverage.

    The settings file in the tests directory is used, therefor the
    environment variable DJANGO_SETTINGS_MODULE is set to 'tests.settings'.
    """
    django.settings_module('tests.settings')
    local('coverage run ./manage.py django test %s' % module)


def coverage_report_plain():
    """
    Runs all tests and prints the coverage report.
    """
    test()
    local('coverage report -m --fail-under=73')


def coverage():
    """
    Runs all tests and builds the coverage html files.

    The index of these files is opened in the webbrowser in the end.
    """
    test()
    local('coverage html')
    webbrowser.open(os.path.join(os.path.dirname(__file__), 'htmlcov', 'index.html'))


def check():
    """
    Checks for PEP 8 errors in openslides and in tests.
    """
    local('flake8 --max-line-length=150 --statistics openslides')
    local('flake8 --max-line-length=150 --statistics tests')


def prepare_commit():
    """
    Does everything that should be done before a commit.

    At the moment it is running the tests and check for PEP 8 errors.
    """
    test()
    check()


def travis_ci():
    """
    Command that is run by Travis CI.
    """
    coverage_report_plain()
    check()


def run_script(script):
    """
    Run a script with the development version of OpenSlides.

    You can find some usefull scripts in extras/scrips/ in the OpenSlides repo.
    """
    os.environ['PYTHONPATH'] = os.path.join(os.path.dirname(__file__))
    os.system("python " + script)
