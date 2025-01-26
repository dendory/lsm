#!/bin/bash

VERSION="0.0.1"

mkdir -p /tmp/lsm-${VERSION}/DEBIAN
mkdir -p /tmp/lsm-${VERSION}/usr/bin
mkdir -p /tmp/lsm-${VERSION}/etc/lsm/manifests
mkdir -p /tmp/lsm-${VERSION}/etc/lsm/states
mkdir -p /tmp/lsm-${VERSION}/etc/lsm/files
mkdir -p /tmp/lsm-${VERSION}/usr/lib/python3/dist-packages
cp ./scripts/lsmlib.py /tmp/lsm-${VERSION}/usr/lib/python3/dist-packages/lsmlib.py
cp ./scripts/lsm-server.py /tmp/lsm-${VERSION}/usr/bin/lsm-server
chmod 755 /tmp/lsm-${VERSION}/usr/bin/lsm-server
# TODO: Add lsm-client and lsm
cp ./lsm.conf /tmp/lsm-${VERSION}/etc/lsm/lsm.conf
echo "Package: LSM" > /tmp/lsm-${VERSION}/DEBIAN/control
echo "Version: ${VERSION}" >> /tmp/lsm-${VERSION}/DEBIAN/control
echo "Section: utils" >> /tmp/lsm-${VERSION}/DEBIAN/control
echo "Priority: optional" >> /tmp/lsm-${VERSION}/DEBIAN/control
echo "Architecture: all" >> /tmp/lsm-${VERSION}/DEBIAN/control
echo "Maintainer: Patrick Lambert <patrick@dendory.ca>" >> /tmp/lsm-${VERSION}/DEBIAN/control
echo "Description: This is a systems configuration management system, similar to Ruby or Chef, but much more lightweight. It doesn't require Java, Apache, Nginx, a database or anything else. It uses the server/client model and stores everything in files within the /etc/lsm folder." >> /tmp/lsm-${VERSION}/DEBIAN/control
dpkg-deb --build /tmp/lsm-${VERSION}
rm -rf /tmp/lsm-${VERSION}
