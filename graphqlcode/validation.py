import os, sys, socket, logging
import fileinput
import variables
import tempfile
import re
import time, threading

hostfile = variables.hostfile
cronfile = variables.cronfile


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
        response = os.system("nc -zv " + hostname +" 8140")
        # and then check the response...
        if response == 0:
            print hostname, 'is up!'
            #logger.info("host %s is up" % hostname)
            return 0
        else:
            print 'trying to  connect again'
        current_try += 1
    return 1
    #print(time.ctime())
    threading.Timer(30, checkConnection).start()

def getHostByAddr(ip_address):
        try:
           name, altname, addr = socket.gethostbyaddr(ip_address)
           #print str(name) + " " + str(altname) + " " + str(addr)
           return name, altname, addr
        except:
            #print "asdf"
            return "none", "none", "none"

def getHostByName(ip_address):
        try:
           addr = socket.gethostbyname(ip_address)
           #print str(name) + " " + str(altname) + " " + str(addr)
           return addr
        except:
            #print "asdf"
            return "none"

def deleteHostEntry(host):
    address = [host]
    oldfile = open(hostfile, "r")
    lines = oldfile.readlines()
    oldfile.close()
    newfile = open(hostfile, "w")
    for line in lines:
        if not any(word in line for word in address):
            newfile.write(line)

    newfile.close()

def setFrequency(time):
    #function to replace time in DeviceCron.sh and deviceCron.sh
    tmpfile = tempfile.NamedTemporaryFile()
    for line in open(cronfile, 'r').readlines():
        oldline = re.sub(r'^echo.*mycron', 'echo \"%d * * * * /opt/puppetlabs/puppet/bin/puppet agent -t\" >> mycron'%time, line)
        print oldline
        tmpfile.write(oldline)
    newfile = open(cronfile, 'w')
    tmpfile.seek(0)
    line = tmpfile.read()
    newfile.write(line)






        

#gethostadd()