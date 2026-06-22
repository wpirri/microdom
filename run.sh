#!/bin/sh

docker run --rm -it \
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

