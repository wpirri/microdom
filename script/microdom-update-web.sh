#!/bin/sh

echo "==== Arbol WEB ===="
rm -rf microdom_web
git clone https://github.com/wpirri/microdom_web.git
cd microdom_web
./install.sh
