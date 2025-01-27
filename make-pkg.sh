#!/bin/bash
#
# Lightweight Systems Manager (LSM) - (C) 2025 Patrick Lambert <patrick@dendory.ca>
# Provided for free under the MIT license.
#
# make-pkg - Creates the .deb file with everything included.
#

VERSION="0.0.14"

# Clean up if needed
rm -rf /tmp/lsm-server-${VERSION}
rm -rf /tmp/lsm-client-${VERSION}
rm -f ./dist/*

# Increment patch level
OLD_VERSION="$VERSION"
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
PATCH=$((PATCH + 1))
VERSION="$MAJOR.$MINOR.$PATCH"

# Server package

# Make temporary folders
mkdir -p /tmp/lsm-server-${VERSION}/DEBIAN
mkdir -p /tmp/lsm-server-${VERSION}/usr/bin
mkdir -p /tmp/lsm-server-${VERSION}/etc/lsm/manifests
mkdir -p /tmp/lsm-server-${VERSION}/etc/lsm/states
mkdir -p /tmp/lsm-server-${VERSION}/etc/lsm/files
mkdir -p /tmp/lsm-server-${VERSION}/usr/lib/python3/dist-packages
mkdir -p /tmp/lsm-server-${VERSION}/lib/systemd/system

# Copy files
cp ./scripts/lsmlib.py /tmp/lsm-server-${VERSION}/usr/lib/python3/dist-packages/lsmlib.py
cp ./scripts/lsm-server.py /tmp/lsm-server-${VERSION}/usr/bin/lsm-server
chmod 755 /tmp/lsm-server-${VERSION}/usr/bin/lsm-server
cp ./scripts/lsm.py /tmp/lsm-server-${VERSION}/usr/bin/lsm
chmod 755 /tmp/lsm-server-${VERSION}/usr/bin/lsm
cp ./misc/lsm.conf /tmp/lsm-server-${VERSION}/etc/lsm/lsm.conf
cp ./misc/lsm-server.service /tmp/lsm-server-${VERSION}/lib/systemd/system/lsm-server.service

# Make debian control file
echo "Package: lsm-server" > /tmp/lsm-server-${VERSION}/DEBIAN/control
echo "Version: ${VERSION}" >> /tmp/lsm-server-${VERSION}/DEBIAN/control
echo "Section: utils" >> /tmp/lsm-server-${VERSION}/DEBIAN/control
echo "Priority: optional" >> /tmp/lsm-server-${VERSION}/DEBIAN/control
echo "Architecture: all" >> /tmp/lsm-server-${VERSION}/DEBIAN/control
echo "Depends: python3, python3-flask, python3-flask-cors" >> /tmp/lsm-server-${VERSION}/DEBIAN/control
echo "Maintainer: Patrick Lambert <patrick@dendory.ca>" >> /tmp/lsm-server-${VERSION}/DEBIAN/control
echo "Description: This is a systems configuration management system, similar to Ruby or Chef, but much more lightweight. It doesn't require Java, Apache, Nginx, a database or anything else. It uses the server/client model and stores everything in files within the /etc/lsm folder." >> /tmp/lsm-server-${VERSION}/DEBIAN/control

# Make config file
echo "/etc/lsm/lsm.conf" > /tmp/lsm-server-${VERSION}/DEBIAN/conffiles

# Make post install script
echo "#!/bin/bash" > /tmp/lsm-server-${VERSION}/DEBIAN/postinst
echo "set -e" >> /tmp/lsm-server-${VERSION}/DEBIAN/postinst
echo "systemctl daemon-reload" >> /tmp/lsm-server-${VERSION}/DEBIAN/postinst
echo "systemctl start lsm-server.service" >> /tmp/lsm-server-${VERSION}/DEBIAN/postinst
echo "systemctl enable lsm-server.service" >> /tmp/lsm-server-${VERSION}/DEBIAN/postinst
echo "exit 0" >> /tmp/lsm-server-${VERSION}/DEBIAN/postinst
chmod 755 /tmp/lsm-server-${VERSION}/DEBIAN/postinst

# Make pre remove script
echo "#!/bin/bash" > /tmp/lsm-server-${VERSION}/DEBIAN/prerm
echo "set -e" >> /tmp/lsm-server-${VERSION}/DEBIAN/prerm
echo "systemctl stop lsm-server.service || true" >> /tmp/lsm-server-${VERSION}/DEBIAN/prerm
echo "systemctl disable lsm-server.service || true" >> /tmp/lsm-server-${VERSION}/DEBIAN/prerm
echo "exit 0" >> /tmp/lsm-server-${VERSION}/DEBIAN/prerm
chmod 755 /tmp/lsm-server-${VERSION}/DEBIAN/prerm

# Create .deb file
sudo chown -R root:root /tmp/lsm-server-${VERSION}
dpkg-deb --build /tmp/lsm-server-${VERSION}
mv /tmp/lsm-server-${VERSION}.deb ./dist/

# Clean up
sudo rm -rf /tmp/lsm-server-${VERSION}


# Client package

# Make temporary folders
mkdir -p /tmp/lsm-client-${VERSION}/DEBIAN
mkdir -p /tmp/lsm-client-${VERSION}/usr/bin
mkdir -p /tmp/lsm-client-${VERSION}/etc/lsm/manifests
mkdir -p /tmp/lsm-client-${VERSION}/etc/lsm/states
mkdir -p /tmp/lsm-client-${VERSION}/etc/lsm/files
mkdir -p /tmp/lsm-client-${VERSION}/usr/lib/python3/dist-packages
mkdir -p /tmp/lsm-client-${VERSION}/etc/cron.d

# Copy files
cp ./scripts/lsmlib.py /tmp/lsm-client-${VERSION}/usr/lib/python3/dist-packages/lsmlib.py
cp ./misc/lsm.conf /tmp/lsm-client-${VERSION}/etc/lsm/lsm.conf
cp ./misc/lsm-client.cron /tmp/lsm-client-${VERSION}/etc/cron.d/lsm
cp ./scripts/lsm-client.py /tmp/lsm-client-${VERSION}/usr/bin/lsm-client
chmod 755 /tmp/lsm-client-${VERSION}/usr/bin/lsm-client
sed -i "s/##VERSION##/${VERSION}/" /tmp/lsm-client-${VERSION}/usr/bin/lsm-client

# Make debian control file
echo "Package: lsm-client" > /tmp/lsm-client-${VERSION}/DEBIAN/control
echo "Version: ${VERSION}" >> /tmp/lsm-client-${VERSION}/DEBIAN/control
echo "Section: utils" >> /tmp/lsm-client-${VERSION}/DEBIAN/control
echo "Priority: optional" >> /tmp/lsm-client-${VERSION}/DEBIAN/control
echo "Architecture: all" >> /tmp/lsm-client-${VERSION}/DEBIAN/control
echo "Depends: python3" >> /tmp/lsm-client-${VERSION}/DEBIAN/control
echo "Maintainer: Patrick Lambert <patrick@dendory.ca>" >> /tmp/lsm-client-${VERSION}/DEBIAN/control
echo "Description: This is a systems configuration management system, similar to Ruby or Chef, but much more lightweight. It doesn't require Java, Apache, Nginx, a database or anything else. It uses the server/client model and stores everything in files within the /etc/lsm folder." >> /tmp/lsm-client-${VERSION}/DEBIAN/control

# Make config file
echo "/etc/lsm/lsm.conf" > /tmp/lsm-client-${VERSION}/DEBIAN/conffiles

# Create .deb file
sudo chown -R root:root /tmp/lsm-client-${VERSION}
dpkg-deb --build /tmp/lsm-client-${VERSION}
mv /tmp/lsm-client-${VERSION}.deb ./dist/

# Clean up
sudo rm -rf /tmp/lsm-client-${VERSION}

# Set new version
sed -i "s/VERSION=\"${OLD_VERSION}\"/VERSION=\"${VERSION}\"/" "$0"
