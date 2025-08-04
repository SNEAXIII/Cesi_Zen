/bin/bash ./wait-for-it.sh api:8000
export NODE_ENV=production
node server.js
