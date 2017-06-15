#!/bin/bash

# Run the server
#python /home/app/src/Service/server.py


#/usr/sbin/sshd
echo "=================================" >> /home/app/log/app.log
date >> /home/app/log/app.log
echo "=================================" >> /home/app/log/app.log
#python /opt/splunk/etc/apps/temp.py >> /home/app/log/app.log 2>> /home/app/log/app.log
service cron start >> /home/app/log/app.log 2>> /home/app/log/app.log
python /home/app/src/Service/server.py >> /home/app/log/app.log 2>> /home/app/log/app.log
        