-- Задача 7, набір 2: початкова схема й дані
CREATE TABLE customer (
    id    integer PRIMARY KEY,
    name  varchar(150) NOT NULL,
    email varchar(120),
    phone varchar(20)
);
CREATE TABLE product (
    id          integer PRIMARY KEY,
    title       varchar(200) NOT NULL,
    price       real,
    category    text,
    legacy_code varchar(10)
);
CREATE TABLE orders (
    id          integer PRIMARY KEY,
    customer_id integer,
    created     date,
    total       real
);
INSERT INTO customer (id, name, email, phone) VALUES
    (1, 'Іван Петренко', 'ivan@example.ua', '0501112233'),
    (2, 'Олена Кравець', 'olena@example.ua', NULL);
INSERT INTO product (id, title, price, category, legacy_code) VALUES
    (1, 'Чайник', 650.5, 'побут', 'P1'),
    (2, 'Склянка', 45, 'побут', NULL);
INSERT INTO orders (id, customer_id, created, total) VALUES
    (1, 1, '2026-09-12', 1296.5),
    (2, 2, '2026-09-13', 45);
