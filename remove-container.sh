#!/usr/bin/env bash
(docker ps -a | grep $1 | awk '{print $1}' | xargs docker stop | xargs docker rm) || :