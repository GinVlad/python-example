from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from scapy.all import *
from multiprocessing import Process, Queue
import Queue as baseQueue


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

def scanport(queue):
	while True:
		port = 0
		try:
			port = queue.get(block=False)
		except baseQueue.Empty:
			return 0
		conf.verb = 0
		resp = sr1(IP(dst=ip)/TCP(sport=RandShort(), dport=port, flags="S"))
		#Check if have TCP layer
		if resp.haslayer(TCP):
			#Check if send success with TCP flag
			if resp.getlayer(TCP).flags == SYNACK:
				#Send ACK packet to confirm
				sr(IP(dst=ip)/TCP(sport=RandShort(), dport=port, flags="A"))
				print "Port " + str(port) + ": Open"

if __name__ == "__main__":
	try: 
		q = Queue()
		for port in range(1, max_port+1):
				q.put(port)
		if check_ip(ip):
			print "Scanning %s..." % ip
			for port in range(1, 5):
				p = Process(target=scanport, args=(q, ))
				p.start()
				p.join()
		else:
			print "Host %s is not connect." % ip
	except Exception:
		sys.exit(1)