#!/usr/bin/env python
"""
	Handles folder compression with tar.
"""

__author__ = "d33pcode"
__copyright__ = "Copyright 2016, HiddenHost"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2016-10-10"

import os
import sys
from utils import questions
import datetime
from dirtools import Dir

def compress(path):
	'''
		Compresses input path to default backup folder
	'''
	d = Dir(path)
	archive_path = generate_archive_path(path)

	if (os.path.exists(archive_path)):
		replace = questions.queryYesNo("WARNING: you already did a backup today. Do you want to replace it?", default="no")
		if not replace:
			sys.exit('Backup canceled.')
	return d.compress_to(archive_path) # the result is the path of the compressed archive

def generate_archive_path(path):
	'''
		example:	/var/backups/lobam/d33pcode-Dev-2016-10-10
	'''
	base_path = '/var/backups/sbam/'
	if (not os.path.exists(base_path)):
		os.makedirs(base_path)

	path_dirs = path.split('/')
	dirname = path_dirs[len(path_dirs)-1]
	time =  str(datetime.date.today())
	return base_path + dirname + '-' + time + '.tar.gz'
