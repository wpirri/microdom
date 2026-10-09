#!/bin/sh

echo "==== Servicio microdom ===="
echo "Stop..."
docker stop microdom
sleep 1
echo "Remove..."
docker rm microdom
sleep 1
echo "Update & Start..."
docker pull ghcr.io/wpirri/microdom:latest
docker run -it \
  -d --restart unless-stopped \
  -e DBUSER=dompi_web \
  -e DBPASSWORD=dompi_web \
  -e DBHOST=192.168.10.5 \
  -e DBNAME=DB_DOMPIWEB \
  --name microdom \
  -v /etc/microdom.conf:/app/etc/microdom.conf \
  -v /var/log/microdom:/app/logs \
  -v /var/lib/microdom/html:/app/html \
  -v /var/lib/microdom/download:/app/download \
  -p 8080:8080 \
  ghcr.io/wpirri/microdom:latest


echo "==== Servicio microdom-task ===="
echo "Stop..."
docker stop microdom-task
sleep 1
echo "Remove..."
docker rm microdom-task
sleep 1
echo "Update & Start..."
docker pull ghcr.io/wpirri/microdom-task:latest
docker run -it \
  -d --restart unless-stopped \
  -e DBUSER=dompi_web \
  -e DBPASSWORD=dompi_web \
  -e DBHOST=192.168.10.5 \
  -e DBNAME=DB_DOMPIWEB \
  --name microdom-task \
  -v /etc/microdom.conf:/app/etc/microdom.conf \
  -v /var/log/microdom:/app/logs \
  -p 8081:8081 \
  ghcr.io/wpirri/microdom-task:latest

echo "==== Arbol WEB ===="
git clone https://github.com/wpirri/microdom_web.git
cd microdom_web
./install.sh
