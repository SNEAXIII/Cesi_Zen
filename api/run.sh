./wait-for-it.sh mariadb:3306
export MODE="prod"
alembic upgrade head
fastapi run