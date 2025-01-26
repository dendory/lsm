#!/usr/bin/python3
#
# Lightweight Systems Manager (LSM) - (C) 2025 Patrick Lambert <patrick@dendory.ca>
# Provided for free under the MIT license.
#
# lsm-server - This is the server daemon.
#

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import subprocess
import lsmlib

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	# This is the only route used

	global conf
	output = {
		'status': 1,
		'message': ""
	}

	output['message'] = "No action specified."
	return jsonify(output)

@app.after_request
def changeserver(response):
	response.headers['Server'] = "LSM"
	return response

if __name__ == '__main__':
	global conf

	conf = lsmlib.load("/etc/lsm/lsm.conf")
	if conf['ssl_key'] != "" and conf['ssl_cert'] != "":
		app.run(host='0.0.0.0', port=int(conf['port']), ssl_context=(conf['ssl_cert'], conf['ssl_key']), threaded=True)
	else:
		app.run(host='0.0.0.0', port=int(conf['port']), threaded=True)
