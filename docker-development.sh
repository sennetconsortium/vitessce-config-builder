#!/bin/bash
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Please supply one of the following (build | up | down | bash | logs)"
    exit 1
fi
arg=$1
if [ "$arg" == "up" ]; then
  if [ $# -eq 1 ]
  then
    echo "No environment supplied. Please supply one of the following (local | dev)"
    exit 1
  fi
  env=$2
  if [ "$env" == "local" ]; then
    echo "===== STARTING LOCAL DOCKER CONFIG ====="
    docker-compose -f docker-compose.yml up -d
  elif [ "$env" == "dev" ]; then
    echo "===== STARTING DEV DOCKER CONFIG ====="
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
  fi
elif [ "$arg" == "build" ]; then
  echo "===== BUILDING IMAGE ====="
  docker build -t vitessce-config-builder .
elif [ "$arg" == "down" ]; then
  echo "===== DOWN ====="
  docker-compose down
elif [ "$arg" == "bash" ]; then
  echo "===== STARTING BASH IN CONTAINER ====="
  docker exec -it vitessce-config-builder bash
elif [ "$arg" == "logs" ]; then
  echo "===== GETTING DOCKER LOGS ====="
  docker logs -f vitessce-config-builder
else
  echo "Invalid argument specified ($1)"
fi