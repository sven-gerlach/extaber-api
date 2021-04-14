#!/bin/bash

curl "http://localhost:8000/comment-votes/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "vote": {
      "comment": "'"${COMM_ID}"'",
      "vote": "'"${VOTE}"'"
    }
  }'

echo
echo
