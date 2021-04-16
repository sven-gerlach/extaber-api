#!/bin/bash

curl "http://localhost:8000/article-votes/${ID}/" \
  --include \
  --request DELETE \
  --header "Authorization: Token ${TOKEN}"

echo
