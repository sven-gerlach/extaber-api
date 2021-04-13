#!/bin/bash

curl "http://localhost:8000/articles/" \
  --include \
  --request GET

echo
echo
