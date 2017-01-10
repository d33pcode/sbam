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
from utils import questions, parser
import datetime
import tarfile
import logging


def compress(path):
    '''
    Stores a folder inside a tar archive compressed with bzip2
    path:
            the full path of the folder to compress
    return:
            the path of the new archive or None
    '''
    archive_path = generate_archive_path(path=path)

    if (os.path.exists(archive_path)):
        replace = questions.queryYesNo(
            "WARNING: you already did a backup today. Do you want to replace it?", default="no")
        if not replace:
            logging.info('Backup canceled.')
            return None
    logging.debug('Creating the bzip2 archive...')
    archive = tarfile.open(archive_path, mode='w:bz2')
    with tarfile.open(archive_path, mode='w:bz2') as archive:
        logging.debug('Looping through subdirs...')
        for subdir, dirs, files in os.walk(path):
            for f in files:
                logging.debug(
                    'Adding ' + os.path.join(subdir, f) + ' to the archive.')
                archive.add(os.path.join(subdir, f))
    return archive_path


def generate_archive_path(path, base_path='/var/backups/sbam/'):
    '''
    Generates a path for the archive.
    path:
            the original path
    base_path:
            the directory in which the archive will be stored
    example:
            /var/backups/sbam/Dev-2016-10-10
    '''
    logging.debug('Geneating archive path...')
    if (not os.path.exists(base_path)):
        os.makedirs(base_path)
    path_dirs = path.split('/')
    dirname = path_dirs[len(path_dirs) - 1]
    time = str(datetime.date.today())
    full_path = base_path + dirname + '-' + time + '.tar.bz2'
    return full_path
