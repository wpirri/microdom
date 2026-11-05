#!/bin/sh

echo "==== FIrmware ===="
wget https://raw.githubusercontent.com/wpirri/dom32-io-wifi/main/Programa-2/pgm.hex
cp -a pgm.hex /var/lib/microdom/download/
rm pgm.hex
wget https://raw.githubusercontent.com/wpirri/dom32-touch/main/Programa-2/domtouch.hex
cp -a domtouch.hex /var/lib/microdom/download/
rm domtouch.hex

