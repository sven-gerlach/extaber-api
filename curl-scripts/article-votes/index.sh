#!/bin/bash

curl "http://localhost:8000/article-votes/" \
  --include \
  --request GET

echo
echo
