#!/usr/bin/env python
"""
Handles folder compression and decompression.
"""

__author__ = "d33pcode"
__copyright__ = "Copyright 2016, HiddenHost"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2016-10-10"

import datetime
import logging
import os
import sys
import tarfile

from utils import parser, questions

# WARNING: this way the archive created contains the whole dir tree!
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
            "WARNING: you already did a backup today. Do you want to replace it?", default="no")    # because of the archive's name
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
                archive.add(os.path.join(subdir, f))    # to avoid full dir tree, cd there THEN add
    return archive_path


def decompress(backup_path, restore_path='.'):
    logging.debug('Opening ' + backup_path + '...')
    tar = tarfile.open(backup_path, "r:bz2")
    for item in tar:
        logging.debug('Extracting ' + str(item) + '...')
        tar.extract(item, restore_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            decompress(item.name, "./" + item.name[:item.name.rfind('/')])


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
    logging.debug('Generating archive path...')
    if (not os.path.exists(base_path)):
        os.makedirs(base_path)
    path_dirs = path.split('/')
    dirname = path_dirs[len(path_dirs) - 1]
    time = str(datetime.date.today())
    full_path = base_path + dirname + '-' + time + '.tar.bz2'
    return full_path
