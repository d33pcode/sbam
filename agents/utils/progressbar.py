#!/usr/bin/env python
"""
	Provides the progress bar
"""

__author__ = "d33pcode"
__copyright__ = "Copyright 2016, HiddenHost"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"
__date__ = "2016-10-13"

from progress.bar import Bar

class ProgressBar():

	def __init__(self, description='Progress', range=20):
		'''
			Initialize the progress bar.
			description:
				the text to display before the actual loading bar
			range:
				the number of steps that will take to get to the finish
			suffix:
				default sets percentage as suffix
		'''
		self.description = description
		self.range = range
		self.steps = 0
		self.bar = Bar(description, max=range, suffix='%(percent)d%%')

	def update(self, steps=1):
		'''
			updates the bar.
			steps:
				the number of times to execute next()
		'''
		for i in range(steps):
			self.bar.next()
			self.steps += 1
			if self.steps == self.range:
				self.bar.finish()
