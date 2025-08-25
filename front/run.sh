set -e
/bin/bash ./wait-for-it.sh api:8000 -t 60 --strict
export NODE_ENV=production
node server.js
