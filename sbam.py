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
import logging
import os
import sys
from datetime import datetime
from getpass import getpass

from tabulate import tabulate

from agents import compressor, encrypter
from agents.databasemanager import DatabaseManager
from agents.utils import parser, questions
from agents.utils.progressbar import ProgressBar
from dirtools import Dir

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

    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    # BACKUP

    if args.folder:
        path = os.path.realpath(args.folder)
        if not (os.path.isdir(path)):
            sys.exit('Please specify a folder.')
        path_dirs = path.split('/')
        dirname = path_dirs[len(path_dirs) - 1]

        logging.info('Compressing ' + dirname + '...')
        compressed_path = compressor.compress(path)

        if (compressed_path):
            logging.info('Done.')
            encrypted = 0
            if args.encrypt:
                encrypted = 1
                key = getpass('Insert a password: ')
                encrypter.encrypt(compressed_path, key)
                logging.info('Backup encrypted.')

            if not args.forget:
                logging.debug('Updating the database...')
                today = datetime.today().isoformat().split('.')[0]
                db_manager = DatabaseManager()
                db_manager.handleTransaction("INSERT OR IGNORE INTO backups(file_path, original_path, backup_date, encrypted) VALUES(\'" +
                                             compressed_path + "\', \'" + path + "\', \'" + today + "\', " + str(encrypted) + ")")
                logging.info('Database updated.')
            else:
                logging.debug(
                    'FORGET option specified: backup not saved to database.')

    # RESTORE

    elif args.backup_path:
        db_manager = DatabaseManager()
        backup_path = ''
        original_path = ''

        if args.backup_path == 'last_backup':
            table = db_manager.listBackups(n=1, enc=True)
            if not table:
                sys.exit('There are no backups in the database.')
        else:
            table = db_manager.listBackups(n=1, backup_path=args.backup_path, enc=True)
            if not table:
                q = args.backup_path + " is not a registered backup. Do you want to restore it anyway?"
                restore = questions.queryYesNo(q, default="no")
                if restore:
                    backup_path = args.backup_path
                    original_path = questions.askForInput(
                        "Insert the restore path.")
                else:
                    sys.exit('Restore canceled.')

        if not backup_path: backup_path = table[0][0]
        if not original_path: original_path = table[0][1]
        enc = table[0][-1]
        logging.debug("backup path: " + backup_path)
        logging.debug("original_path: " + original_path)
        if enc:
            logging.info('The selected backup is encrypted.')
            key = getpass('Insert the password: ')  # add support for wrong passwords!
            logging.debug('Decrypting...')
            encrypter.decrypt(backup_path+".enc", backup_path, key)
        logging.debug('Decompressing...')
        compressor.decompress(backup_path, restore_path=original_path)
        logging.info('Backup restored to ' + original_path)

    # LIST

    if args.entries_number:
        db_manager = DatabaseManager()
        table = db_manager.listBackups(args.entries_number)
        if not table:
            logging.info("There are no backups here.")
        else:
            headers = ['backup path', 'original path', 'date']
            print tabulate(table, headers, tablefmt="fancy_grid")
