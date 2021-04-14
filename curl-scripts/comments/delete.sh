#!/bin/bash

curl "http://localhost:8000/comments/${ID}/" \
  --include \
  --request DELETE \
  --header "Authorization: Token ${TOKEN}"

echo
echo
