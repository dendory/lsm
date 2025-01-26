#!/usr/bin/python3
#
# Lightweight Systems Manager (LSM) - (C) 2025 Patrick Lambert <patrick@dendory.ca>
# Provided for free under the MIT license.
#
# LSMLIB - This is the utilities library.
#

import re
import os
import sys
import time
import json
import uuid
import time
import string
import random
import socket
import datetime
import logging
import logging.handlers
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

def syslog():
	# Return a logger handle
	log = logging.getLogger("LSM")
	log.setLevel(logging.DEBUG)
	handler = logging.handlers.SysLogHandler(address = '/dev/log')
	handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
	log.addHandler(handler)
	return log

def resolve(ip):
	# Try to resolve an IP address
	try:
		hostname = socket.gethostbyaddr(ip)
		return hostname[0]
	except:
		return ""

def base36(number):
	# Convert an int to alphanum
	base36 = ""
	alphabet = string.digits + string.ascii_uppercase
	while int(number) > 0:
		number, i = divmod(int(number), len(alphabet))
		base36 = alphabet[i] + base36
	return base36

def make_id():
	# Return a unique ID
	hw = str(base36(uuid.getnode() + int(time.time()*1000000)))
	pad = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(12-len(hw)))
	return str(hw + pad).lower()

def load(filename):
	# Load a JSON file and return the content as a dict
	with open(filename, 'r', encoding='UTF-8') as fd:
		data = fd.read()
	return json.loads(data)

def save(filename, data):
	# Save data to a file in JSON format
	with open(filename, 'w', encoding='UTF-8') as fd:
		fd.write(json.dumps(data, sort_keys = False, indent = 4))

def now():
	# Return the current date and time as a string
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def since(timestamp):
	# Return the number of seconds since a specific timestamp
	x = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
	y = datetime.datetime.strptime(now(), "%Y-%m-%d %H:%M:%S")
	z = y - x
	return z.seconds

def connect(url):
	# Connect to an endpoint and return the content of a JSON reply
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36 LSM'
	}
	con = urllib.request.Request(url, headers=headers)
	cj = CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	stream = opener.open(con)
	result = stream.read()
	charset = stream.info().get_param('charset', "utf8")
	b = result.decode(charset)
	return json.loads(b)

def alphanum(text, symbols=False, spaces=False):
	# Return only alphanumerical characters
	if spaces and symbols:
		return re.sub('[^0-9a-zA-Z \_\-\.\[\]\(\)\@\!\?\:\'\;]+', '', text)
	elif spaces:
		return re.sub('[^0-9a-zA-Z ]+', '', text)
	elif symbols:
		return re.sub('[^0-9a-zA-Z\_\-\.\[\]\(\)\@\!\?\:\'\;]+', '', text)
	return re.sub('[^0-9a-zA-Z]+', '', text)
