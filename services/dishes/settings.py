# CREATE USER 'antifragile_user'@'localhost' IDENTIFIED BY 'antifragile_password';
# CREATE DATABASE antifragile;
# GRANT ALL PRIVILEGES ON antifragile.* TO 'antifragile_user'@'localhost';
# ALTER TABLE ingredients MODIFY name VARCHAR(100) CHARACTER SET utf8;

# sudo apt install postgresql postgresql-contrib
# createuser --interactive
# createdb -O antifragile_user antifragile
# sudo -u antifragile_user psql antifragile

DB_NAME = 'antifragile'
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USERNAME = 'antifragile_user'
DB_PASSWORD = 'antifragile_password'
