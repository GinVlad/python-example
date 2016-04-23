#!/usr/bin/python

import os
import sys


for (root, dirs, files) in os.walk(sys.argv[1]):
	print str((len(root.split('/'))-1) * '----') + root
	for file in files:
		print str(len(root.split('/')) * '----') + file

