#!/bin/bash

curl "http://localhost:8000/article-votes/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "vote": {
      "article": "'"${ART_ID}"'",
      "vote": "'"${VOTE}"'"
    }
  }'

echo
echo
