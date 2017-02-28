#!/usr/bin/env python
"""
Simple Backup Manager.

The main class interprets user's arguments as request for the agents.
"""

__author__ = "d33pcode"
__copyright__ = "Copyright 2016, HiddenHost"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2016-10-10"

import argparse
import datetime
import logging
import os
import sys
from getpass import getpass

from tabulate import tabulate

from agents import compressor, encrypter
from agents.databasemanager import DatabaseManager
from agents.utils import parser, questions
from agents.utils.progressbar import ProgressBar
from dirtools import Dir


def backup_table(n):
    """
    A list of the first n backups.
    """
    db_manager = DatabaseManager()
    table = db_manager.listBackups(n)
    if not table:
        logging.info("There are no backups here.")
        return
    else:
        headers = ['backup path', 'original path', 'date']
        return tabulate(table, headers, tablefmt="fancy_grid")


def backup(folder, encrypt, forget):
    """
    Creates a new backup.
    folder:
        the path to the folder to compress
    encrypt:
        encrypts the folder if True
    forget:
        does not create a new database entry if True
    """
    path = os.path.realpath(folder)
    if not (os.path.isdir(path)):
        sys.exit('Please specify a folder.')
    path_dirs = path.split('/')
    dirname = path_dirs[len(path_dirs) - 1]

    logging.info('Compressing ' + dirname + '...')
    compressed_path = compressor.compress(path)

    if (compressed_path):
        logging.info('Done.')
        if encrypt:
            key = getpass('Insert a password: ')
            encrypter.encrypt(compressed_path, key)
            logging.info('Backup encrypted.')
        if not forget:
            logging.debug('Updating the database...')
            today = datetime.datetime.today().isoformat().split('.')[0]
            db_manager = DatabaseManager()
            db_manager.handleTransaction("INSERT OR IGNORE INTO backups(file_path, original_path, backup_date, encrypted) VALUES(\'" +
                                         compressed_path + "\', \'" + path + "\', \'" + today + "\', " + str(int(encrypt)) + ")")
            logging.info('Database updated.')
        else:
            logging.debug(
                'FORGET option specified: backup not saved to database.')
    return compressed_path


def restore(folder):
    """
    Restores a backup.
    folder:
        the path to the folder to decompress
    """
    db_manager = DatabaseManager()
    backup_path = ''
    original_path = ''

    if folder == 'last_backup':
        table = db_manager.listBackups(n=1, enc=True)
        if not table:
            sys.exit('There are no backups in the database.')
    else:
        table = db_manager.listBackups(n=1, backup_path=folder, enc=True)
        if not table:
            q = folder + " is not a registered backup. Do you want to restore it anyway?"
            restore = questions.queryYesNo(q, default="no")
            if restore:
                backup_path = folder
                original_path = questions.askForInput(
                    "Insert the restore path.")
            else:
                sys.exit('Restore canceled.')

    if not backup_path:
        backup_path = table[0][0]
    if not original_path:
        original_path = table[0][1]
    enc = table[0][-1]
    logging.debug("backup path: " + backup_path)
    logging.debug("original path: " + original_path)
    if enc:
        logging.info('The selected backup is encrypted.')
        # add support for wrong passwords!
        key = getpass('Insert the password: ')
        logging.debug('Decrypting...')
        encrypter.decrypt(backup_path + ".enc", backup_path, key)
    logging.debug('Decompressing...')
    compressor.decompress(backup_path, restore_path=original_path)
    logging.info('Backup restored to ' + original_path)


def verbosity(v):
    l = logging.DEBUG if v else logging.INFO
    return logging.basicConfig(format='%(message)s', level=l)


if __name__ == '__main__':
    if not os.geteuid() == 0:  # check root privileges
        sys.exit('Administrator privileges are required.')

    parser = argparse.ArgumentParser(
        prog='sbam',
        description='Simple Backup Manager.',
        epilog='Enjoy.',
    )

    parser.add_argument('-l', '--list', dest='entries_number', type=int,
                        nargs='?', const=3, help='List the last N backups (default: 3)')
    parser.add_argument('-f', '--folder', dest='folder',
                        help='The folder to backup')
    parser.add_argument('-r', '--restore', dest='backup_path', nargs='?', const='last_backup',
                        help='Restore a backup from [BACKUP_PATH] if exists (default: last backup)')
    # parser.add_argument('-d', '--drive', dest='drive_path', help = 'Specify
    # an external drive for backup')
    parser.add_argument('-e', '--encrypt',
                        help='Encrypt the folder', action='store_true')
    parser.add_argument(
        '-F', '--forget', help="Don't save this backup in the database", action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='Display verbose output', action='store_true')
    args = parser.parse_args()

    # LOGGING
    verbosity(args.verbose)

    # BACKUP
    if args.folder:
        backup(args.folder, args.encrypt, args.forget)

    # RESTORE
    elif args.backup_path:
        restore(args.backup_path)

    # LIST
    if args.entries_number:
        print backup_table(args.entries_number)
