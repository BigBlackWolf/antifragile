INSERT INTO dishes(name) VALUES ('Пюре'), ('Борщ'), ('Рагу');
INSERT INTO ingredients(id, name) VALUES (1, 'Огурец'), (2, 'Помидор'), (3, 'Картошка');
INSERT INTO dishes_ingredients(dish_id, ingredient_id, quantity)
VALUES
       (1, 3, 5),
       (2, 2, 1),
       (2, 3, 4),
       (3, 1, 2),
       (3, 2, 2),
       (3, 3, 2);