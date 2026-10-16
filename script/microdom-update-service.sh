#!/bin/sh

echo "==== Servicio microdom ===="
docker pull ghcr.io/wpirri/microdom:latest
sleep 1
docker restart microdom

echo "==== Servicio microdom-task ===="
docker pull ghcr.io/wpirri/microdom-task:latest
sleep 1
docker restart microdom-task

echo "==== Servicio microdom-abm ===="
docker pull ghcr.io/wpirri/microdom-abm:latest
sleep 1
docker restart microdom-abm
