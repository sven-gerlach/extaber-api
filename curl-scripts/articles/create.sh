#!/bin/bash

curl "http://localhost:8000/articles/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "article": {
      "headline": "'"${HL}"'",
      "body": "'"${BODY}"'"
    }
  }'

echo
echo
