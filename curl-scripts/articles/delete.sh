#!/bin/bash

curl "http://localhost:8000/articles/${ID}/" \
  --include \
  --request DELETE \
  --header "Authorization: Token ${TOKEN}"

echo
