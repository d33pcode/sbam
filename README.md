# Sbam
---
[![Build Status](https://travis-ci.org/d33pcode/sbam.svg?branch=master)](https://travis-ci.org/d33pcode/sbam)

Sbam is a Python2 utility that aims to help you manage your backups with ease.

It provides functions to backup and restore directories, list the current backups and optional password protection, too.


### Installation
---
- Clone the project
- Install the requirements with `pigar -c` (remember to `sudo pip install pigar`)
- `sudo ln -s /path/to/sbam/sbam.py /usr/bin/sbam` to use it outside its folder. In the rest of this file I'll assume you can run `sbam` from everywhere in the terminal. If you skip this step, you can use `./sbam.py` inside your installation folder.

### Basic usage
---

To compress a folder, simply use:
```
sbam -f folder/to/compress
```
Sbam will compress it in `/var/backups/sbam` and automatically register the newly created backup.
You can restore it with `sbam -r`.

The restore function, without arguments, will decompress your last backup and move it to its original path.
You can optionally specify a folder to restore:
```
sbam -r folder/to/restore
```
Note that this will work even if the folder does not longer exist. That's because sbam stores by default its backups in a small sqlite database.
To see a list of your last backups, simply use:
```
sbam -l                           # lists the last 3 backups
sbam -l 10                        # lists the last 10 backups
```
**Warning:** Sbam keeps track of your backup date, too. If you already backed up a folder today, any other backup of that folder will replace the previous one.


### Encryption
---
The `-e` option will encrypt the compressed folder and password-protect it.
```
sbam -ef folder/to/backup
```
This will prompt you for a password.

If you don't want Sbam to register your backup, use the `--forget` option while backing up the folder:
```
sbam -Ff folder/to/compress
```
This backup will be stored in `/var/backups/sbam` too, but it will not be shown in the list.
Note: the list is automatically updated every time `sbam -l` is called. This means that if you manually remove a backup, the entry will be removed from the database, too.
