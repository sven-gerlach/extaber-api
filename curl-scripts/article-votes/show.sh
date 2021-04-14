#!/bin/bash

curl "http://localhost:8000/article-votes/${ID}/" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}"

echo
echo
