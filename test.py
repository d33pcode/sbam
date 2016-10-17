#!/usr/bin/env python
"""
	This is a test class.

	Nothing to see here.
"""

__author__ = "d33pcode"
__copyright__ = "Copyright 2016, HiddenHost"
__credits__ = ""
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2016-10-13"

from agents.utils.progressbar import ProgressBar
import threading

def foo():
	while True:
		pass

q = Queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()

s = q.get()
print s
