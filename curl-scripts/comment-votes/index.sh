#!/bin/bash

curl "http://localhost:8000/comment-votes/" \
  --include \
  --request GET \
  --header "Accept: application/json; indent=2"

echo
echo
