import argparse
import logging
import os
import sqlite3
import sys
from datetime import datetime
from getpass import getpass

from tabulate import tabulate

import sbam
from agents import compressor, encrypter
from agents.databasemanager import DatabaseManager
from agents.utils import parser, questions
from agents.utils.progressbar import ProgressBar
from dirtools import Dir


def test_list():
    try:
        config_dir = '/home/' + os.environ['SUDO_USER'] + '/.config/sbam/'
    except KeyError:
        config_dir = '/home/' + os.environ['USER'] + '/.config/sbam/'
    db_path = config_dir + 'sbam.db'
    print db_path
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    select = "select file_path, original_path, backup_date from backups order by backup_date desc limit 5"
    backups = [e for e in cur.execute(select)]
    conn.close()
    headers = ['backup path', 'original path', 'date']
    assert tabulate(backups, headers,
                    tablefmt="fancy_grid") == sbam.backup_table(5)


#
# def test_backup():
#
#
# def test_restore():
#
#
# def test_encrypt():
#
#
# def test_verbose():
