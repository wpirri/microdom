#!/bin/sh

sudo mkdir -p /var/log/microdom
sudo chmod 0777 /var/log/microdom
sudo cp -uva etc/microdom.conf /etc

echo "Building microdom docker image..."
docker build -t microdom .
echo "Stop microdom..."
docker stop microdom
sleep 1
echo "Remove microdom..."
docker rm microdom
sleep 1
echo "Run microdom..."
docker run -it \
  -d --restart unless-stopped \
  -e DBUSER=dompi_web \
  -e DBPASSWORD=dompi_web \
  -e DBHOST=192.168.10.32 \
  -e DBNAME=DB_DOMPIWEB \
  --name microdom \
  -v /etc/microdom.conf:/app/etc/microdom.conf \
  -v /var/log/microdom:/app/logs \
  -v /var/lib/microdom/html:/app/html \
  -v /var/lib/microdom/download:/app/download \
  -p 8080:8080 microdom

