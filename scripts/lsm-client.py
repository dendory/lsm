#!/usr/bin/python3
#
# Lightweight Systems Manager (LSM) - (C) 2025 Patrick Lambert <patrick@dendory.ca>
# Provided for free under the MIT license.
#
# lsm-client - The client script.
#

import urllib.parse
import lsmlib
import os

log = lsmlib.syslog()

# Load config file
try:
	conf = lsmlib.load("/etc/lsm/lsm.conf")
except:
	log.warning("Could not parse config file: /etc/lsm/lsm.conf")
	exit(1)

# Load existing state
try:
	state = lsmlib.load("/etc/lsm/states/localhost")
except:
	state = {
		'id': lsmlib.make_id(),
		'status': "All good."
	}

# Check current state


# Try to find the machine's hostname
hostname = ""
try:
	hostname = os.environ['HOSTNAME']
except:
	try:
		with open("/etc/hostname", "r") as fd:
			hostname = fd.read().split()[0].split('\n')[0]
	except:
		pass

# Connect to server
try:
	if hostname != "":
		url = "{}?id={}&name={}&status={}&version=##VERSION##".format(conf['server'], state['id'], str(hostname).split('.')[0], urllib.parse.quote_plus(state['status']))
	else:
		url = "{}?id={}&status={}&version=##VERSION##".format(conf['server'], state['id'], urllib.parse.quote_plus(state['status']))
	manifest = lsmlib.connect(url)
except:
	log.warning("Could not connect to server: {}".format(url))
	exit(1)

# Do any new actions


# Save new state
lsmlib.save("/etc/lsm/states/localhost", state)

exit(0)
