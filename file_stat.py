#!/usr/bin/env python

import os, sys

file = os.stat(sys.argv[1])

if file:
	print "Filename: %s" % sys.argv[1]
	print "File size: %d" % file.st_size
	print "Owner by: %d" %file.st_uid
else:
	print "File not found"
