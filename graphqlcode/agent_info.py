import os, sys, socket, logging
import logging
import subprocess
import fileinput
import variables
import tempfile
import re
import time, threading



configFile = variables.configFile
logger = logging.getLogger('Agent_Info')
hostfile = variables.hostfile
cronfile = variables.cronfile
#host = variables.host


def myrun(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        logger.info(line),
        if line == '' and p.poll() != None:
            break
    #return ''.join(stdout)
    return p.returncode

def StartScript(ip_address, hostname):
    logger.info("Start Script")

    logger.info("running change config file")
    newhost = "server = " + hostname + "\n"
    address = ["server"]
    oldfile = open(configFile, 'r')
    lines = oldfile.readlines()
    oldfile.close()
    newfile = open(configFile, "w")
    for line in lines:
        if not any(word in line for word in address):
            newfile.write(line)
    newfile.write(newhost)
    newfile.close()

    logger.info("running change host file")
    outputfile = open(variables.hostfile, 'a+')
    entry = ip_address + "\t" + hostname + "\n"
    if entry not in outputfile:
        outputfile.writelines(entry)
    outputfile.close()

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
            threading.Timer(30, checkConnection).start()
            return 0
        else:
            print 'trying to  connect again'
        current_try += 1
    disconnect(hostname)
    variables.connection = 1
    return 1


def getHostByAddr(ip_address):
    try:
        name, altname, addr = socket.gethostbyaddr(ip_address)
        # print str(name) + " " + str(altname) + " " + str(addr)
        return name, altname, addr
    except:
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

def setFrequency(timer):
    #function to replace time in DeviceCron.sh and deviceCron.sh
    tmpfile = tempfile.NamedTemporaryFile()
    for line in open(cronfile, 'r').readlines():
        oldline = re.sub(r"^echo.*mycron", "echo \"%d * * * * /opt/puppetlabs/puppet/bin/puppet agent -t\" >> mycron"%timer, line)
        print oldline
        tmpfile.write(oldline)
    newfile = open(cronfile, 'w')
    tmpfile.seek(0)
    line = tmpfile.read()
    newfile.write(line)

def disconnect(host):
    deleteHostEntry(host)
    clear_agent_certs = ['rm', '-rf', '/opt/puppetlabs/puppet/cache/devices/apic.cisco.com/ssl']
    clear_device_certs = ['rm', '-rf', '/etc/puppetlabs/puppet/ssl']

    myrun(clear_agent_certs)
    myrun(clear_device_certs)

def runDevice():
    run_agent_command = ['puppet', 'device', '--debug']
    if myrun(run_agent_command) == 0:
        return 0
    else:
        return 1