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
	log = lsmlib.syslog()
	output = {
		'status': 1,
		'message': ""
	}

	if 'id' not in request.args and 'status' not in request.args: # Missing arguments
		output['message'] = "Arguments missing."
		log.warning("Client {}[]: {}".format(request.remote_addr, output['message']))
		return jsonify(output)

	id = lsmlib.alphanum(request.args['id'])
	status = lsmlib.alphanum(request.args['status'], spaces=True)
	hostname = lsmlib.resolve(request.remote_addr)
	if hostname == "" and 'name' in request.args:
		hostname = lsmlib.alphanum(request.args['name'])

	if len(id) != 12: # Check if ID looks valid
		output['message'] = "Invalid ID."
		log.warning("Client {}[]: {}".format(request.remote_addr, output['message']))
		return jsonify(output)

	try: # Existing client
		state = lsmlib.load("/etc/lsm/states/{}".format(id))
		if state['ip'] != request.remote_addr:
			if str(conf['allow_ip_changes']).lower() != "yes":
				output['message'] = "IP changes not allowed."
				log.warning("Client {}[{}]: {}".format(request.remote_addr, id, output['message']))
				return jsonify(output)
		state['ip'] = request.remote_addr
		state['timestamp'] = lsmlib.now()
		state['status'] = status
		state['hostname'] = hostname
	except: # New client
		state = {
			'id': id,
			'ip': request.remote_addr,
			'hostname': hostname,
			'timestamp': lsmlib.now(),
			'status': status,
			'approved': 'no'
		}
		log.warning("Client {}[{}]: New connection.".format(request.remote_addr, id))

	# Save client
	lsmlib.save("/etc/lsm/states/{}".format(id), state)

	output['message'] = "OK"
	output['status'] = 0
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
