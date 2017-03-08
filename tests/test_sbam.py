#!/usr/bin/env python
"""
SBaM main testing module.
"""
import argparse
import datetime
import logging
import os
import sqlite3
import sys
from getpass import getpass

from tabulate import tabulate

import sbam
from agents import compressor, encrypter
from agents.databasemanager import DatabaseManager
from agents.utils import questions
from agents.utils.progressbar import ProgressBar
from dirtools import Dir


def test_list():
    try:
        config_dir = '/home/' + os.environ['SUDO_USER'] + '/.config/sbam/'
    except KeyError:
        config_dir = '/home/' + os.environ['USER'] + '/.config/sbam/'
    db_path = config_dir + 'sbam.db'
    # needs to be executed first, cause it cleans the db too
    sbam_table = sbam.backup_table(5)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    select = "select file_path, original_path, backup_date from backups order by backup_date desc limit 5"
    backups = [e for e in cur.execute(select)]
    conn.close()
    headers = ['backup path', 'original path', 'date']
    test_table = tabulate(backups, headers, tablefmt="fancy_grid")
    assert test_table == sbam_table


def test_verbose():
    test_logger = logging.basicConfig(format='%(message)s', level=logging.INFO)
    assert test_logger == sbam.verbosity(True)


def test_backup():
    p = 'tests/test_backup/'
    if not os.path.isdir(p):
        os.makedirs(p)
    with open(p + 'test_file', 'w') as f:
        f.write('Test ' + str(datetime.date.today()))
    sbam_archive_path = sbam.backup(p, False, False)
    test_archive_path = '/var/backups/sbam/test_backup-' + \
        str(datetime.date.today()) + '.tar.bz2'
    test_result = sbam_archive_path == test_archive_path
    os.remove(p + 'test_file')
    os.remove(sbam_archive_path)
    os.removedirs(p)
    assert test_result
#
# def test_restore():
#
#
# def test_encrypt():
#
#
