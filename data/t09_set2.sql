-- Задача 9, набір 2: схема й дані
CREATE TABLE customer (
    id    integer CONSTRAINT pk_customer PRIMARY KEY,
    email varchar(120) NOT NULL CONSTRAINT uq_customer_email UNIQUE
);
CREATE TABLE product (
    id    integer CONSTRAINT pk_product PRIMARY KEY,
    title varchar(200) NOT NULL,
    price numeric(10,2) NOT NULL CONSTRAINT ck_product_price CHECK (price > 0),
    stock integer NOT NULL DEFAULT 0
);
CREATE TABLE orders (
    id          bigint CONSTRAINT pk_orders PRIMARY KEY,
    customer_id integer NOT NULL CONSTRAINT fk_orders_customer REFERENCES customer (id),
    status      varchar(12) NOT NULL CONSTRAINT ck_orders_status CHECK (status IN ('new', 'paid', 'shipped', 'cancelled'))
);
INSERT INTO customer (id, email) VALUES (1, 'ivan@example.ua'), (2, 'olena@example.ua');
INSERT INTO product (id, title, price, stock) VALUES (1, 'Чайник', 650.00, 5), (2, 'Склянка', 45.00, 100);
INSERT INTO orders (id, customer_id, status) VALUES (1, 1, 'new'), (2, 2, 'paid');
