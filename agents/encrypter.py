#!/usr/bin/env python
"""
    Provides methods for encryption and decryption using Blowfish.
"""

__author__ = "d33pcode"
__copyright__ = "Copyright 2016, HiddenHost"
__credits__ = "adamb70 @ github"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2016-10-11"

import os
from struct import pack

from Crypto.Cipher import _Blowfish


def encrypt(in_filepath, key):
    '''
        Encrypt the specified file with the specified
        key and output to the chosen output file.
    '''
    out_filepath = in_filepath + '.enc'
    size = os.path.getsize(in_filepath)
    infile = open(in_filepath, 'rb')
    outfile = open(out_filepath, 'wb')
    data = infile.read()
    infile.close()

    if size % 8 > 0:  # Add padding if size if not divisible by 8
        extra = 8 - (size % 8)
        padding = [0] * extra
        padding = pack('b' * extra, *padding)
        data += padding

    revdata = reverseBytes(data)
    encrypted_data = encryptBytes(revdata, key)
    finaldata = reverseBytes(encrypted_data)
    outfile.write(finaldata)
    outfile.close()
    os.remove(in_filepath)  # new backup is stored as compressed_path.enc


def decrypt(in_filepath, out_filepath, key):
    '''
        Decrypt the specified file with the specified
        key and output to the chosen output file
    '''
    infile = open(in_filepath, 'rb')
    outfile = open(out_filepath, 'wb')
    data = infile.read()
    infile.close()

    revdata = reverseBytes(data)
    decrypted_data = decryptBytes(revdata, key)
    finaldata = reverseBytes(decrypted_data)

    end = len(finaldata) - 1
    while str(finaldata[end]).encode('hex') == '00':
        end -= 1

    finaldata = finaldata[0:end]

    outfile.write(finaldata)
    outfile.close()


def encryptBytes(data, key):
    cipher = _Blowfish.new(key, _Blowfish.MODE_ECB)
    return cipher.encrypt(data)


def decryptBytes(data, key):
    cipher = _Blowfish.new(key, _Blowfish.MODE_ECB)
    return cipher.decrypt(data)


def reverseBytes(data):
    '''
        Takes data and reverses byte order to fit
        blowfish-compat format. For example, using
        reverseBytes('12345678') will return 43218765.
    '''
    data_size = 0
    for n in data:
        data_size += 1

    reversedbytes = bytearray()
    i = 0
    for x in range(0, data_size / 4):
        a = (data[i:i + 4])
        i += 4
        z = 0

        n0 = a[z]
        n1 = a[z + 1]
        n2 = a[z + 2]
        n3 = a[z + 3]
        reversedbytes.append(n3)
        reversedbytes.append(n2)
        reversedbytes.append(n1)
        reversedbytes.append(n0)
    return buffer(reversedbytes)
