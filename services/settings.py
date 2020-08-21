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

DB_NAME = 'd3j96te1p86pgb'
DB_HOST = 'ec2-54-247-78-30.eu-west-1.compute.amazonaws.com'
DB_PORT = 5432
DB_USERNAME = 'knooejhchvacqp'
DB_PASSWORD = '6243dcb6bed248fc29c3b45028c0a9ab571202f7c5978b1008132610aeaf51a4'
APP_HOST = 'https://antifragile-cookbook.herokuapp.com/'
APP_PORT = 8080
ROOT_FOLDER = pathlib.Path(__file__).parent.parent
