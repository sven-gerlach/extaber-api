#!/bin/bash

curl "http://localhost:8000/get-user-details/" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}" \
  --header "Accept: application/json; indent=2"

echo
