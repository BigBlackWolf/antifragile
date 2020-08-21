# CREATE USER 'antifragile_user'@'localhost' IDENTIFIED BY 'antifragile_password';
# CREATE DATABASE antifragile;
# GRANT ALL PRIVILEGES ON antifragile.* TO 'antifragile_user'@'localhost';
# ALTER TABLE ingredients MODIFY name VARCHAR(100) CHARACTER SET utf8;

# sudo apt install postgresql postgresql-contrib
# createuser --interactive
# createdb -O antifragile_user antifragile
# sudo -u antifragile_user psql antifragile
# https://dish.co.nz/recipes/leftover-lamb-ragu-2020
# tree -I 'venv|__pycache__|*.pyc|.pytest_cache|css|js|scripts|images|fonts|test.py'
# select ingredients.name as ingr, dishes_ingredients.quantity, dishes.name from dishes_ingredients join dishes on dishes_ingredients.dish_id = dishes.id join ingredients on dishes_ingredients.ingredient_id = ingredients.id;
# drop table dishes, dishes_ingredients,ingredients cascade;
import pathlib

DB_NAME = 'antifragile'
DB_HOST = 'antifragile-cookbook.herokuapp.com'
DB_PORT = 5432
DB_USERNAME = 'antifragile_user'
DB_PASSWORD = 'antifragile_password'
APP_HOST = 'https://antifragile-cookbook.herokuapp.com/'
APP_PORT = 8080
ROOT_FOLDER = pathlib.Path(__file__).parent.parent
