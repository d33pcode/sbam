#!/usr/bin/env python
"""
	Provides utilities for database creation and manteinance.

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
__date__ = "2016-10-11"

import sqlite3
from os import environ as env
from os.path import isfile, getsize

class DatabaseManager:

	db_path = "sbam.db"

	def __init__(self):
		self.buildDatabase()

	def buildDatabase(self):
		self.handleTransaction( """
			CREATE TABLE IF NOT EXISTS backups (
				id INTEGER PRIMARY KEY AUTOINCREMENT ,
				file_path TEXT,
				original_path TEXT,
				backup_date DATE,
				synced BOOLEAN
			);
		""")

	def destroyDatabase(self):
		self.handleTransaction("DROP TABLE IF EXISTS backups")

	def handleTransaction(self, *commands):
		'''
			- Opens a connection to the SQLite database
			- If database is opened successfully, it returns a connection object
			- If given database name does not exist then this call will create the database
			- Executes every command
		'''
		connection = sqlite3.connect(self.db_path)
		cursor = connection.cursor()

		for command in commands:
			cursor.execute(command)

		connection.commit() # save changes
		connection.close() # don't EVER leave a connection open!

	def addBackup(self, file_path, original_path, backup_date, synced):
		connection = sqlite3.connect(self.db_path)
		cursor = connection.cursor()
		cursor.executemany("INSERT INTO backups(file_path, original_path, backup_date, synced) VALUES (?,?,?,?)", [file_path, original_path, backup_date, synced])

		connection.commit()
		connection.close()

	def listBackups(self, n=1, backup_path=None):
		'''
			Returns a list of the last n backups
			ordered by date
		'''
		connection = sqlite3.connect(self.db_path)
		cursor = connection.cursor()
		backups = []
		if backup_path:
			query = "select original_path from backups where file_path = \'%s\' order by backup_date desc limit %s" % (backup_path, str(n))
		else:
			query = "select original_path from backups order by backup_date desc limit " + str(n)
		for entry in cursor.execute(query):
			backups.append(entry)
		connection.close()
		return backups
