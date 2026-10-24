#!/bin/sh

echo "==== Servicio microdom ===="
docker stop microdom
docker rm microdom
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
docker stop microdom-task
docker rm microdom-task
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

echo "==== Servicio microdom-abm ===="
docker stop microdom-abm
docker rm microdom-abm
docker pull ghcr.io/wpirri/microdom-abm:latest
docker run -it \
  -d --restart unless-stopped \
  -e DBUSER=dompi_web \
  -e DBPASSWORD=dompi_web \
  -e DBHOST=192.168.10.5 \
  -e DBNAME=DB_DOMPIWEB \
  --name microdom-abm \
  -v /etc/microdom.conf:/app/etc/microdom.conf \
  -v /var/log/microdom:/app/logs \
  -v /var/lib/microdom/html:/app/html \
  -v /var/lib/microdom/download:/app/download \
  -p 8083:8083 \
  ghcr.io/wpirri/microdom-abm:latest
