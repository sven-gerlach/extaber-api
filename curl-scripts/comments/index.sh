#!/bin/bash

curl "http://localhost:8000/comments/" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}" \

echo
echo
