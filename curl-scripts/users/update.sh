#!/bin/bash

curl "http://localhost:8000/update-user-details/" \
  --include \
  --request PATCH \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "user": {
      "username": "'"${UN}"'",
      "user_img_url": "'"${IMG}"'"
    }
  }'

echo
