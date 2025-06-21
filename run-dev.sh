#!/bin/bash
# Run docker redis and leetcode api for development
docker-compose --file docker-compose.dev.yml --env-file .env up