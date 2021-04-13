#!/bin/bash

curl "http://localhost:8000/articles/${ID}/" \
  --include \
  --request PATCH \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "article": {
      "headline": "'"${HL}"'",
      "body": "'"${BODY}"'",
      "owner": "'"${OWNER}"'"
    }
  }'

echo
