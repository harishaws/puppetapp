import os, sys, socket, logging
import fileinput

logger = logging.getLogger('validation')
hostfile = '/etc/hosts'


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def checkConnection(hostname):
    max_number_of_tries = 2
    current_try = 0
    while current_try < max_number_of_tries:
    	response = os.system("ping -c 5 " + hostname)
    	# and then check the response...
    	if response == 0:
        	print hostname, 'is up!'
        	logger.info("host %s is up" % hostname)
         	return True
    	else:
        	print 'trying to  connect again'
        current_try += 1
    return False


def gethost(ip_address):
    address = [ip_address]
    oldfile = open(hostfile, "r")
    lines = oldfile.readlines()
    oldfile.close()
    newfile = open(hostfile, "w")
    for line in lines:
        if not any(word in line for word in address):
            newfile.write(line)

    newfile.close()
    try:
        name, altname, addr = socket.gethostbyaddr(ip_address)
        return name, altname, addr
    except:
        return "none", "none", "none"