set -e
./wait-for-it.sh mariadb:3306 -t 60 --strict
export MODE="prod"
alembic upgrade head
fastapi run