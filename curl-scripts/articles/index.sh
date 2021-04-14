#!/bin/bash

curl "http://localhost:8000/articles/" \
  --include \
  --request GET \
  --header "Accept: application/json; indent=2"

echo
echo
