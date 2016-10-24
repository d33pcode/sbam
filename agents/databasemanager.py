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
import os

class DatabaseManager:

	config_dir =os.environ['HOME'] +'/.config/sbam/'
	db_path = config_dir + 'sbam.db'

	def __init__(self):
		if not os.path.isdir(self.config_dir):
			os.makedirs(self.config_dir)
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
			Opens a connection to the SQLite database;
			If given database name does not exist,
			then this call will create the database
			Executes every command
		'''
		connection = sqlite3.connect(self.db_path)
		with connection:	# automatically commit and close
			cursor = connection.cursor()
			for command in commands:
				cursor.execute(command)

	def addBackup(self, file_path, original_path, backup_date, synced):
		connection = sqlite3.connect(self.db_path)
		with connection:
			cursor = connection.cursor()
			cursor.executemany("INSERT INTO backups(file_path, original_path, backup_date, synced) VALUES (?,?,?,?)", [file_path, original_path, backup_date, synced])

	def listBackups(self, n=3, backup_path=None):
		'''
			Returns a list of the last n backups
			ordered by date
		'''
		self.cleanDb()
		connection = sqlite3.connect(self.db_path)
		cursor = connection.cursor()
		backups = []
		if backup_path:
			query = "select file_path, original_path, backup_date from backups where file_path = \'%s\' order by backup_date desc limit %s" % (backup_path, str(n))
		else:
			query = "select file_path, original_path, backup_date from backups order by backup_date desc limit " + str(n)
		for entry in cursor.execute(query):
			backups.append(entry)
		connection.close()
		return backups

	def cleanDb(self):
		'''
			Cleans the database
			removing entries that no longer exist
		'''
		query = "select file_path from backups"
		connection = sqlite3.connect(self.db_path)
		with connection:
			cursor = connection.cursor()
			results = []
			cursor.execute(query)
			for res in cursor.fetchall():
				folder = res[0]
				if not os.path.exists(folder):
					cursor.execute("delete from backups where file_path = \'%s\'" % folder) # sorry for that, but i couldn't find any better way.
		return results
