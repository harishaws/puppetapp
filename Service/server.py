from flask import Flask, Markup, redirect, url_for, render_template, request
import agent_info as agent
import validation
import json
import sys
import socket
import urllib
# from cobra.model.pol import Uni as PolUni
# from cobra.model.aaa import UserEp as AaaUserEp
# from cobra.model.aaa import AppUser as AaaAppUser
# from cobra.model.aaa import UserCert as AaaUserCert
import json
import threading
import logging
import base64

app = Flask(__name__, template_folder="../UIAssets", static_folder="../UIAssets")


@app.route('/')
def index():
    return "hello world"


@app.route('/run_agent.json', methods=['GET', 'POST'])
def run_agent():
    app.logger.info('FORM DATA SENDING...')

    ip_address = request.json["ip_address"]
    message = ""
    # hostname = request.json["hostname"]

    app.logger.info('-- Values received:')
    app.logger.info('ip_address: {}'.format(ip_address))

    name, altname, address = validation.gethost("%s" % ip_address)
    if not name == "none":
        agent.StartScript(address[0], name)
    elif not validation.is_valid_ipv4_address(ip_address):  # checks the IP address to see if it's valid.
        app.logger.info('Ip address invalid or hostname not reachable')

    elif validation.checkConnection("%s" % ip_address):
        app.logger.info('ip reachable but no DNS configured')

    app.logger.info('Thread started')

    return "hello world"


if __name__ == '__main__':
    fStr = '%(asctime)s %(levelname)5s %(name)s(%(lineno)s) %(message)s'
    logging.basicConfig(filename="/home/app/log/puppet.log", format=fStr, level=logging.DEBUG)
    logging.basicConfig(filename="/home/app/log/acisession.log", format=fStr, level=logging.DEBUG)
    app.run(debug=True, host='0.0.0.0', port=80)

    # if __name__ == '__main__':
    #     # Setup logging
    #     fStr='%(asctime)s %(levelname)5s %(message)s'
    #     logging.basicConfig(filename='/home/app/log/server.log', format=fStr, level=logging.DEBUG)
    #
    #     # Run app flask server
    #     app.run(host='0.0.0.0', port=80)