#!/usr/bin/env bash
source ./globals.sh
docker run \
	-d \
	-p 5556:5556 \
	-p 7001:7001 \
	-p 7002:7002 \
	-p 7003:7003 \
	-p 7004:7004 \
	--name=weblogic \
	-h node-manager \
	-v $(pwd):/mnt/host/$(pwd) \
	--entrypoint=/bin/bash \
	$IMAGE_NAME \
	-c 'startNodeManager.sh & wlst.sh /mnt/host/'$(pwd)'/context/startAll.wlst.py & tail --retry -f $DOMAIN_HOME/servers/AdminServer/logs/AdminServer.out' \
	| xargs docker logs -f