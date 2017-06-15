import logging
import subprocess
import fileinput

configFile = "/etc/puppetlabs/puppet/puppet.conf"
hostfile = '/etc/hosts'
logger = logging.getLogger('Agent_Info')


def myrun(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        logger.info(line),
        if line == '' and p.poll() != None:
            break
    return ''.join(stdout)


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
    outputfile = open(hostfile, 'a+')
    entry = ip_address + "\t" + hostname + "\n"
    if entry not in outputfile:
        outputfile.writelines(entry)
    outputfile.close()

    host = '%s' % hostname
    run_agent_command = ['puppet', 'device', '--debug', '--trace', '--server', host, '--deviceconfig',
                         '/etc/puppetlabs/puppet/device.conf']
    clear_certs = ['rm', '-rf', '/opt/puppetlabs/puppet/cache/devices/apic.cisco.com/ssl']
    logger.info("------running agent command-------")
    myrun(clear_certs)
    myrun(run_agent_command)