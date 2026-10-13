#!/usr/bin/env sh
set -eu
: "${RAPIDAPI_KEY:?Set your own subscribed RapidAPI application key}"
curl --fail-with-body --silent --show-error --max-time 15 \
  'https://crm-lead-hygiene-api.p.rapidapi.com/v1/contact/normalize' \
  --header "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  --header 'X-RapidAPI-Host: crm-lead-hygiene-api.p.rapidapi.com' \
  --header 'Content-Type: application/json' \
  --data-binary '@contact.json'
