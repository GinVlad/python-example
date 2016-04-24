#!/usr/bin/env python

"""
Author: GinVlad
Reference:  [*] http://www.secdev.org/projects/scapy/doc/usage.html#tcp-syn-traceroute
			[*] http://www.tcpipguide.com/free/t_TCPConnectionEstablishmentProcessTheThreeWayHandsh-3.htm
			[*]	http://rapid.web.unc.edu/resources/tcp-flag-key/
"""

from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from scapy.all import *
import sys
import threading
import Queue


ip = raw_input("IP: ")
max_port = int(raw_input("Input range port to scan: "))
SYNACK = 0x12 #SYN-ACK TCP flag
def check_ip(ip):
	conf.verb=0 #Hide output send packet
	#sc1() to send packet and receive first response
	resp = sr1((IP(dst=ip)/ICMP()), timeout=10)
	if resp.haslayer(ICMP):
		return True
	else:
		return False

class scanport(threading.Thread):
	def __init__(self, lock, queue):
		threading.Thread.__init__(self)
		self.lock = lock
		self.queue = queue

	def run(self):
		while True:
			conf.verb=0 #Hide output send packet
			#get port from queue
			port = queue.get()
			#Send SYN packet to check port open
			resp = sr1(IP(dst=ip)/TCP(sport=RandShort(), dport=port, flags="S"))
			#Check if have TCP layer
			if resp.haslayer(TCP):
				#Check if send success with TCP flag
				if resp.getlayer(TCP).flags == SYNACK:
					#Send ACK packet to confirm
					sr(IP(dst=ip)/TCP(sport=RandShort(), dport=port, flags="A"))
					with lock:
						print "Port " + str(port) + ": Open"
						break
				else:
					with lock:
						break
			else:
				with lock:
					break
			self.queue.task_done()

if __name__ == '__main__':
	try: 
		lock = threading.Lock()
		queue = Queue.Queue(5)
		if check_ip(ip):
			print "Scanning %s..." % ip
			for port in range(1, max_port+1):
				queue.put(port)
				scan = scanport(queue, lock)
				scan.start()
			queue.join()
		else:
			print "Host %s is not connect." % ip
	except Exception:
		sys.exit(1)
