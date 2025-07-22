#!/bin/bash

ENV=$1

if [[ "$ENV" == "dev" ]]; then
  cp config/environment/.env.dev config/environment/.env
  echo "Switched to DEV environment"
elif [[ "$ENV" == "prod" ]]; then
  cp config/environment/.env.production config/environment/.env
  echo "Switched to PROD environment"
else
  echo "Usage: ./switch_env.sh [dev|prod]"
  exit 1
fi
