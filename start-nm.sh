#!/usr/bin/env bash
source ./globals.sh
docker run -d -p 5556:5556 -p 7002:7002 -p 7003:7003 -p 7004:7004 --name=node-manager -h node-manager --entrypoint=startNodeManager.sh $IMAGE_NAME
