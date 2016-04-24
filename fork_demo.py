#!/usr/bin/env python
import os

def child_process():
	print "I am the child process and my PID is: %d" % os.getpid()
	print "The child is exiting"
	print "The parent process PID is: %d" % os.getppid()

def parent_process():
	print "I am the parent process with PID: %d" % os.getpid()
	childpid = os.fork()
	if childpid == 0:
		print "We are inside the child process"
		child_process()
	else:
		print "We are inside the parent process"
		print "The child has the PID: %d" %childpid
	while True:
		pass

parent_process()