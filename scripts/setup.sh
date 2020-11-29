#! /bin/bash

virtualenv -p python3.8 .env || exit 1
echo "export PYTHONPATH=\"$PYTHONPATH:$(pwd)\"" >> .env/bin/activate
