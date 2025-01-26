#!/usr/bin/python3
#
# Lightweight Systems Manager (LSM) - (C) 2025 Patrick Lambert <patrick@dendory.ca>
# Provided for free under the MIT license.
#
# lsm - The command line utility.
#

import lsmlib
import sys
import os

if len(sys.argv) == 1:
	print("Lightweight Systems Manager (LSM) - Command line utility")
	print()
	print("Usage:")
	print("\tlist           - List all known hosts")
	print("\tapprove <id>   - Approve a specific host")
	print("\tunapprove <id> - Remove approval for a specific host")
	exit(1)

if str(sys.argv[1]) == "list":
	for id in os.listdir("/etc/lsm/states"):
		if len(id) == 12:
			state = lsmlib.load("/etc/lsm/states/{}".format(id))
			if state['hostname'] != "":
				print("* {}[{}]".format(state['hostname'], id))
			else:
				print("* {}[{}]".format(state['ip'], id))
			print("Last check-in: {} ({:,} secs ago)".format(state['timestamp'], lsmlib.since(state['timestamp'])))
			print("Last status: {}".format(state['status']))
			print("Approved: {}".format(state['approved']))
			print()
			exit(0)

elif str(sys.argv[1]) == "approve" and len(sys.argv) == 3:
	state = lsmlib.load("/etc/lsm/states/{}".format(sys.argv[2]))
	state['approved'] = "yes"
	lsmlib.save("/etc/lsm/states/{}".format(sys.argv[2]), state)
	print("Approved: yes")
	exit(0)

elif str(sys.argv[1]) == "unapprove" and len(sys.argv) == 3:
	state = lsmlib.load("/etc/lsm/states/{}".format(sys.argv[2]))
	state['approved'] = "no"
	lsmlib.save("/etc/lsm/states/{}".format(sys.argv[2]), state)
	print("Approved: no")
	exit(0)

else:
	print("Unknown command.")
	exit(1)
