-- Задача 9, набір 1: схема й дані
CREATE TABLE publisher (
    id   integer CONSTRAINT pk_publisher PRIMARY KEY,
    name varchar(120) NOT NULL
);
CREATE TABLE book (
    id           integer CONSTRAINT pk_book PRIMARY KEY,
    title        varchar(200) NOT NULL,
    isbn         char(13) CONSTRAINT uq_book_isbn UNIQUE,
    publisher_id integer NOT NULL CONSTRAINT fk_book_publisher REFERENCES publisher (id),
    price        numeric(8,2) NOT NULL CONSTRAINT ck_book_price CHECK (price >= 0),
    pages        smallint
);
INSERT INTO publisher (id, name) VALUES (1, 'Фабула'), (2, 'Основи');
INSERT INTO book (id, title, isbn, publisher_id, price, pages) VALUES
    (1, 'Місто', '9789660000011', 1, 250.50, 640),
    (2, 'Тигролови', '9789660000028', 2, 180.00, 288);
