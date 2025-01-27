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
	print("\tlist-hosts                                        - List all known hosts")
	print("\tapprove <id>                                      - Approve a host")
	print("\tunapprove <id>                                    - Remove approval for a host")
	print("\tlist-manifests                                    - List all manifests")
	print("\tnew-manifest <manifest name>                      - Create a new manifest")
	print("\tremove-manifest <manifest name>                   - Remove a manifest")
	print("\tshow-manifest <manifest name>                     - Show information about a manifest")
	print("\tattach <manifest name> <id>                       - Attach a manifest to a host")
	print("\tadd-file-to-manifest <manifest name> <file path>  - Add a file to a manifest")
	print("\tadd-include-to-manifest <manifest name>           - Add one manifest to another")
	print("\tadd-service-to-manifest <manifest name>           - Add a service to a manifest")
	print("\tadd-package-to-manifest <manifest name>           - Add a package to a manifest")
	exit(1)

if str(sys.argv[1]) == "list-hosts":
	for id in os.listdir("/etc/lsm/states"):
		if len(id) == 12:
			state = lsmlib.load("/etc/lsm/states/{}".format(id))
			if state['hostname'] != "":
				print(lsmlib.bold("* {} - {} [{}]".format(state['hostname'], state['ip'], id)))
			else:
				print(lsmlib.bold("* {} [{}]".format(state['ip'], id)))
			print("Last check-in: {} ({:,} secs ago)".format(state['timestamp'], lsmlib.since(state['timestamp'])))
			print("Client version: {}".format(state['version']))
			print("Approved: {}".format(state['approved']))
			print("Manifests:")
			for manifest in state['manifests']:
				print("- {}".format(manifest))
			print("Last status:")
			for status in str(state['status']).split('##'):
				print("- {}".format(status))
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
