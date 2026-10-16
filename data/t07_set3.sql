-- Задача 7, набір 3: початкова схема й дані
CREATE TABLE study_group (code varchar(20) PRIMARY KEY, title varchar(100));
CREATE TABLE student (
    id         integer PRIMARY KEY,
    name       varchar(150) NOT NULL,
    group_code varchar(20),
    birth_date date,
    stipend    real,
    temp_flag  boolean
);
CREATE TABLE lesson (
    id       integer PRIMARY KEY,
    held_at  timestamp,
    duration smallint,
    topic    text
);
INSERT INTO study_group (code, title) VALUES ('G-101', 'Перша група'), ('G-102', 'Друга група');
INSERT INTO student (id, name, group_code, birth_date, stipend, temp_flag) VALUES
    (1, 'Андрій Шевчук', 'G-101', '2008-04-15', 1200.5, false),
    (2, 'Ірина Лис', 'G-102', '2008-09-03', NULL, true);
INSERT INTO lesson (id, held_at, duration, topic) VALUES
    (1, '2026-09-14 08:30', 80, 'Вступ'),
    (2, '2026-09-15 10:10', 80, NULL);
