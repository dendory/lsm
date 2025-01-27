# Lightweight Systems Manager (LSM)

This is a systems configuration management system, similar to Ruby or Chef, but much more lightweight. It doesn't require Java, Apache, Nginx, a database or anything else. It uses the server/client model and stores everything in files within the `/etc/lsm` folder. It supports Debian/Ubuntu for the server component, and Debian/Ubuntu and Windows for the client. The server part is based on Python's Flask library, and all errors are sent to the system's syslog.


## Installation

LSM comes as two packages: server and client. If you download the source, you can use the `make-pkg.sh` script to create the package files. Or you can download the packages directly and install them like this
* Server: `sudo dpkg -i lsm-server-1.0.0.deb`
* Clients: `sudo dpkg -i lsm-client-1.0.0.deb`


## Configuration

The main configuration file is in `/etc/lsm/lsm.conf` in JSON format. You need to configure it for your environment on both the clients and server. Here are the configuration files:

### port (server only)
The port number to listen on.

### server (client only)
The URL of the server, in this format: `http://server.example.com:port/`

### ssl_cert (server only)
The location of your SSL certificate if you want to use HTTPS. If you use Certbot that would be `/etc/letsencrypt/live/server.example.com/fullchain.pem`

### ssl_key (server only)
The location of your SSL key if you want to use HTTPS. If you use Certbot that would be `/etc/letsencrypt/live/server.example.com/privkey.pem`

### allow_ip_changes (server only)
Whether to allow clients that have registered to connect again from a different IP. This may be an insecure option to set.


## Commands

The `lsm` utility has a number of commands that can be used to interact with the system. Here are the commands available:

### list
List all known hosts

### approve <id>
Approve a host

### unapprove <id>
Remove approval for a host


## Author

This code was created by: Patrick Lambert <patrick@dendory.ca>


## License

Copyright 2025, Patrick Lambert

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
