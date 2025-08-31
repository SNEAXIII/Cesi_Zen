set -e
/bin/bash ./wait-for-it.sh api:8000 -t 60 --strict
node server.js
