#!/bin/bash

curl "http://localhost:8000/comment-votes/" \
  --include \
  --request GET

echo
echo
