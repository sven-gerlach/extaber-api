#!/bin/bash

curl "http://localhost:8000/articles/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "article": {
      "img_url": "'"${URL}"'",
      "title": "'"${TITLE}"'",
      "sub_title": "'"${SUB}"'",
      "body": "'"${BODY}"'"
    }
  }'

echo
echo
