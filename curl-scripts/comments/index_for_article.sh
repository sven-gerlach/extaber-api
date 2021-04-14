#!/bin/bash

curl "http://localhost:8000/comments/${ID}/" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}" \
  --header "Accept: application/json; indent=2"

echo
echo
