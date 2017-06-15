import requests
import json
import logging
import base64

# from OpenSSL.crypto import FILETYPE_PEM, load_privatekey

APIC_URL = 'https://172.17.0.1'  # Fixed, APIC's gateway for the app
KEY_FILE_PATH = '/home/app/credentials/plugin.key'  # Fixed for every app
APP_USER = 'Cisco_proxyagent'
USER_CERT = APP_USER
USER_CERT_DN = 'uni/userext/appuser-{}/usercert-{}'.format(APP_USER, USER_CERT)


def requestAppToken():
    session = requests.session()

    try:
        from OpenSSL.crypto import FILETYPE_PEM, load_privatekey, sign
    except:
        logging.info("=== could not import openssl crypto ===")

    ### Login Using RequestAppToken ###
    uri = "/api/requestAppToken.json"
    app_token_payload = {"aaaAppToken": {"attributes": {"appName": APP_USER}}}

    data = json.dumps(app_token_payload)
    payLoad = "POST" + uri + data

    p_key = ''
    with open(KEY_FILE_PATH, "r") as file:
        p_key = file.read()
    p_key = load_privatekey(FILETYPE_PEM, p_key)

    signedDigest = sign(p_key, payLoad.encode(), 'sha256')
    signature = base64.b64encode(signedDigest).decode()

    cookie = "APIC-Request-Signature=" + signature + ";"
    cookie += "APIC-Certificate-Algorithm=v1.0;"
    cookie += "APIC-Certificate-Fingerprint=fingerprint;"
    cookie += "APIC-Certificate-DN=" + USER_CERT_DN

    reply = session.post("{}{}".format(APIC_URL, uri), data=data, headers={'Cookie': cookie}, verify=False)
    json_reply = json.loads(reply.text)
    logging.info("Reply of requestAppToken: {}".format(json_reply))
    auth_token = json_reply['imdata'][0]['aaaLogin']['attributes']['token']
    # print auth_token
    token_cookie = {}
    token_cookie['APIC-Cookie'] = auth_token
    return token_cookie


def main():
    result = requestAppToken()
    # queryUrl = 'http://172.17.0.1/api/class/fvTenant.json'
    # response = requests.get(queryUrl, cookies = result, verify=False)
    resp_json = json.dumps(result)
    print resp_json
    # print response
    # finalResult=json.dumps(result)
    # print result
    # print type(resp_json)
    return resp_json


if __name__ == '__main__':
    main()