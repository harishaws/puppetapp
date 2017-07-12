#!/bin/bash

#write out current crontab
crontab -r
#echo new cron into cron file
echo "* * * * * /opt/puppetlabs/puppet/bin/puppet agent -t" >> mycron
#install new cron file
crontab mycron
rm mycron