#!/bin/sh

docker build -t microdom:latest .
docker tag microdom:latest ghcr.io/wpirri/microdom:latest
docker push ghcr.io/wpirri/microdom:latest

