#!/usr/bin/env bash
source ./globals.sh
docker run -d -p 7001:7001 --name=$ADMIN_SERVER_CONTAINER --link $NODE_MANAGER_CONTAINER:node-manager --entrypoint=startWebLogic.sh $IMAGE_NAME