#!/usr/bin/python3
#
# Lightweight Systems Manager (LSM) - (C) 2025 Patrick Lambert <patrick@dendory.ca>
# Provided for free under the MIT license.
#
# lsm-server - This is the server daemon.
#

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
import subprocess
import lsmlib

app = Flask(__name__)
log = lsmlib.syslog()
CORS(app)

def process_manifest(manifest):
	# Process a manifest file

	global conf, log
	output = []
	data = lsmlib.load("/etc/lsm/manifests/{}".format(manifest))

	for entry in data:
		if str(entry['type']).lower() == "file":
			output.append({
				'type': "file",
				'fetch': entry['fetch'],
				'before': entry['before'],
				'after': entry['after'],
				'user': entry['user'],
				'group': entry['group'],
				'chmod': entry['chmod'],
				'filename': entry['filename']
			})
		elif str(entry['type']).lower() == "include":
			output += process_manifest(entry['manifest'])
		elif str(entry['type']).lower() == "service":
			output.append({
				'type': "service",
				'name': entry['name'],
				'state': entry['state']
			})
		else:
			log.warning("Unknown manifest type: {}".format(entry['type']))

	return output

@app.route('/', methods=['GET', 'POST'])
def index():
	# This is the main connect endpoint

	global conf, log
	output = {
		'status': 1,
		'message': "",
		'manifest': []
	}

	if 'id' not in request.args or 'status' not in request.args or 'version' not in request.args: # Missing arguments
		output['message'] = "Arguments missing."
		log.warning("Client {}[]: {}".format(request.remote_addr, output['message']))
		return jsonify(output)

	id = lsmlib.alphanum(request.args['id'])
	status = lsmlib.alphanum(request.args['status'], spaces=True, symbols=True)
	version = lsmlib.alphanum(request.args['version'], spaces=False, symbols=True)
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
		state['version'] = version
		state['hostname'] = hostname
	except: # New client
		state = {
			'id': id,
			'ip': request.remote_addr,
			'hostname': hostname,
			'timestamp': lsmlib.now(),
			'version': version,
			'status': status,
			'approved': 'no',
			'manifests': []
		}
		log.warning("Client {}[{}]: New connection.".format(request.remote_addr, id))

	# Save state
	lsmlib.save("/etc/lsm/states/{}".format(id), state)

	# Process manifest
	if state['approved'] == "yes":
		for manifest in manifests:
			output['manifest'] += process_manifest(manifest)

	output['message'] = "OK"
	output['status'] = 0
	return jsonify(output)

@app.route('/fetch/<filename>')
def sendstuff(filename):
	# Download a file

	return send_from_directory("/etc/lsm/files", lsmlib.alphanum(filename, Symbols=True))

@app.after_request
def changeserver(response):
	response.headers['Server'] = "LSM"
	return response

if __name__ == '__main__':
	global conf

	conf = lsmlib.load("/etc/lsm/lsm-server.conf")
	if conf['ssl_key'] != "" and conf['ssl_cert'] != "":
		app.run(host='0.0.0.0', port=int(conf['port']), ssl_context=(conf['ssl_cert'], conf['ssl_key']), threaded=True)
	else:
		app.run(host='0.0.0.0', port=int(conf['port']), threaded=True)
