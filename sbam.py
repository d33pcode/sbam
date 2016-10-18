#!/usr/bin/env python
"""
	Simple Backup Manager.

	Detailed description.
	Lorem ipsum dolor sit amet, consectetur adipisicing elit,
	sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
	Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
	ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
	in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
"""

__author__ = "d33pcode"
__copyright__ = "Copyright 2016, HiddenHost"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2016-10-10"

import os, sys, argparse
from getpass import getpass
from dirtools import Dir
from datetime import datetime
from agents import compressor, encrypter
from agents.databasemanager import DatabaseManager
from agents.utils.progressbar import ProgressBar
from tabulate import tabulate

if __name__ == '__main__' :

	if not os.geteuid() == 0:   # check root privileges
		sys.exit('Administrator privileges are required.')

	parser = argparse.ArgumentParser(
		prog='sbam',
		description='Simple Backup Manager.',
		epilog='Enjoy.',
	)

	parser.add_argument('-l', '--list', dest='entries_number', type=int, nargs='?', const=3, help = 'List the last N backups (default: 3)')
	parser.add_argument('-f' , '--folder', dest='folder', help = 'The folder to backup')
	parser.add_argument('-r', '--restore', dest='restore_path', nargs='?', const='last_backup', help = 'Restore a backup for [RESTORE_PATH] if exists (default: last backup)')
	parser.add_argument('-d', '--drive', dest='drive_path', help = 'Specify an external drive for backup')
	parser.add_argument('-e', '--encrypt', help = 'Encrypt the folder', action = 'store_true')
	parser.add_argument('-F', '--forget', help = "Don't save this backup in the database", action = 'store_true')
	parser.add_argument('-v', '--verbose', help = 'Display verbose output', action = 'store_true')
	args = parser.parse_args()

	if args.folder:
		path = args.folder.replace('~', os.environ['HOME'])
		if not args.folder.startswith('/'):
			sys.exit('Please specify the full path.')
		path_dirs = path.split('/')
		dirname = path_dirs[len(path_dirs)-1]

		print 'Compressing ' + dirname + '...'
		compressed_path = compressor.compress(path)
		print 'Done.'

		if args.encrypt:
			key = getpass('Insert a password: ')
			encrypter.encrypt(compressed_path, compressed_path + '.enc', key)
			os.remove(compressed_path) # new backup is stored as compressed_path.enc
			print 'Backup encrypted.'

		if not args.forget:
			print 'Updating the database...'
			today = str(datetime.today()).split(' ')[0]
			db_manager = DatabaseManager()
			db_manager.handleTransaction("INSERT INTO backups(file_path, original_path, backup_date, synced) VALUES(\'" + compressed_path + "\', \'" + path + "\', \'" + today + "\', " + "0" + ")")
			print 'Database updated.'

	elif args.restore_path:
		if args.restore_path == 'last_backup':
			db_manager = DatabaseManager()
			table = db_manager.listBackups(1)
			backup_path = table[0][0]
			original_path = table[0][1]
			print "backup path: " + backup_path
			print "original_path: " + original_path
		else:
			print 'you specified a backup'

	elif args.entries_number:
		db_manager = DatabaseManager()
		table = db_manager.listBackups(args.entries_number)
		headers = ['backup path', 'original path', 'date']
		print tabulate(table, headers, tablefmt="fancy_grid")
	else:
		parser.print_help()
