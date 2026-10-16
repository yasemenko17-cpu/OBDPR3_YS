-- Задача 9, набір 3: схема й дані
CREATE TABLE study_group (
    id   integer CONSTRAINT pk_study_group PRIMARY KEY,
    code varchar(20) NOT NULL CONSTRAINT uq_group_code UNIQUE
);
CREATE TABLE student (
    id             integer CONSTRAINT pk_student PRIMARY KEY,
    full_name      varchar(150) NOT NULL,
    study_group_id integer NOT NULL CONSTRAINT fk_student_group REFERENCES study_group (id),
    record_book    char(8) NOT NULL,
    stipend        numeric(7,2) CONSTRAINT ck_student_stipend CHECK (stipend >= 0)
);
INSERT INTO study_group (id, code) VALUES (1, 'G-101'), (2, 'G-102');
INSERT INTO student (id, full_name, study_group_id, record_book, stipend) VALUES
    (1, 'Андрій Шевчук', 1, 'KN000001', 1200.00),
    (2, 'Ірина Лис', 2, 'KN000002', NULL);
