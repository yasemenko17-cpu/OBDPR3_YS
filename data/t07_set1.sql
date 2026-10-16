-- Задача 7, набір 1: початкова схема й дані
CREATE TABLE publisher (id integer PRIMARY KEY, name varchar(120) NOT NULL);
CREATE TABLE book (
    id          integer PRIMARY KEY,
    title       varchar(200) NOT NULL,
    publisher_id integer,
    year        smallint,
    price       real,
    isbn        varchar(20),
    legacy_code varchar(10)
);
INSERT INTO publisher (id, name) VALUES (1, 'Фабула'), (2, 'Основи');
INSERT INTO book (id, title, publisher_id, year, price, isbn, legacy_code) VALUES
    (1, 'Місто', 1, 1999, 250.5, '9789660000011', 'L1'),
    (2, 'Тигролови', 2, 1944, 180, '9789660000028', 'L2'),
    (3, 'Intermezzo', 1, 1901, 99.99, '9789660000035', NULL);
