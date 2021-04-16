#!/bin/bash

curl "http://localhost:8000/comment-votes/${ID}/" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}" \
  --header "Accept: application/json; indent=2"

echo
echo
