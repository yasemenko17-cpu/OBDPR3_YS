"""Допоміжні засоби тестів: підключення до PostgreSQL, тимчасова схема, читання каталогу.

Параметри підключення беруться зі змінних середовища PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
(у Codespaces їх задає devcontainer; локально за замовчуванням localhost:5432, користувач postgres).
"""
import os
import re
import uuid

import psycopg

CODES = {"a": "NO ACTION", "r": "RESTRICT", "c": "CASCADE", "n": "SET NULL", "d": "SET DEFAULT"}


def connect():
    return psycopg.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", "postgres"),
        dbname=os.environ.get("PGDATABASE", "postgres"),
        autocommit=True,
        connect_timeout=5,
    )


class ScriptError(Exception):
    """SQL-скрипт студента завершився помилкою."""

    def __init__(self, error):
        self.state = error.sqlstate
        super().__init__(f"{error.sqlstate}: {str(error).strip().splitlines()[0]}")


class Db:
    """З'єднання з окремою тимчасовою схемою: усі таблиці тесту створюються лише в ній."""

    def __init__(self):
        self.conn = connect()
        self.schema = "t_" + uuid.uuid4().hex[:10]
        self.conn.execute(f"CREATE SCHEMA {self.schema}")
        self.conn.execute(f"SET search_path = {self.schema}")

    def close(self):
        try:
            self.conn.execute("SET search_path = public")
            self.conn.execute(f"DROP SCHEMA IF EXISTS {self.schema} CASCADE")
        finally:
            self.conn.close()

    def run(self, sql):
        """Виконує скрипт (кілька команд). Помилку перетворює на ScriptError."""
        try:
            self.conn.execute(sql)
        except psycopg.Error as error:
            raise ScriptError(error) from None

    def rows(self, sql, params=None):
        return self.conn.execute(sql, params).fetchall()

    def value(self, sql, params=None):
        row = self.conn.execute(sql, params).fetchone()
        return row[0] if row else None


def canon(type_name):
    """Приводить запис типу до вигляду, який повертає format_type()."""
    t = re.sub(r"\s+", " ", type_name.strip().lower())
    t = re.sub(r"^varchar\b", "character varying", t)
    t = re.sub(r"^char\b", "character", t)
    t = re.sub(r"^timestamptz\b", "timestamp with time zone", t)
    t = re.sub(r"^timestamp(?!\s+with)(?=$|\()", "timestamp without time zone", t)
    t = {"int": "integer", "int4": "integer", "int8": "bigint", "int2": "smallint", "bool": "boolean"}.get(t, t)
    return t


def table_oid(db, table):
    return db.value("SELECT to_regclass(%s)::oid", (table,))


def tables(db):
    return sorted(r[0] for r in db.rows(
        "SELECT relname FROM pg_class WHERE relnamespace = current_schema()::regnamespace AND relkind IN ('r', 'p')"))


def columns(db, table):
    """{ім'я: {type, notnull, identity, generated, default}} у порядку створення."""
    rows = db.rows(
        """SELECT a.attname, format_type(a.atttypid, a.atttypmod), a.attnotnull, a.attidentity, a.attgenerated,
                  pg_get_expr(d.adbin, d.adrelid)
           FROM pg_attribute a LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
           WHERE a.attrelid = to_regclass(%s) AND a.attnum > 0 AND NOT a.attisdropped ORDER BY a.attnum""",
        (table,))
    return {r[0]: {"type": r[1], "notnull": r[2], "identity": r[3], "generated": r[4], "default": r[5]} for r in rows}


def constraints(db, table):
    """Обмеження таблиці (p, f, u, c): список словників."""
    rows = db.rows(
        """SELECT c.conname, c.contype,
                  ARRAY(SELECT a.attname FROM unnest(c.conkey) WITH ORDINALITY k(n, o)
                        JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = k.n ORDER BY k.o),
                  (SELECT relname FROM pg_class WHERE oid = c.confrelid),
                  ARRAY(SELECT a.attname FROM unnest(c.confkey) WITH ORDINALITY k(n, o)
                        JOIN pg_attribute a ON a.attrelid = c.confrelid AND a.attnum = k.n ORDER BY k.o),
                  c.confdeltype, c.confupdtype, c.condeferrable, c.condeferred,
                  (SELECT i.indnullsnotdistinct FROM pg_index i WHERE i.indexrelid = c.conindid),
                  pg_get_constraintdef(c.oid)
           FROM pg_constraint c
           WHERE c.conrelid = to_regclass(%s) AND c.contype IN ('p', 'f', 'u', 'c') ORDER BY c.conname""",
        (table,))
    keys = ("name", "type", "cols", "ref", "refcols", "on_delete", "on_update", "deferrable", "deferred", "nnd", "def")
    return [dict(zip(keys, r)) for r in rows]


class Outcome:
    """Результат спроби: sqlstate (порожній, якщо помилки не було), обмеження, стовпець, повідомлення, значення verify."""

    def __init__(self, state="", constraint=None, column=None, message="", value=None):
        self.state, self.constraint, self.column, self.message, self.value = state, constraint, column, message, value


def attempt(db, setup, statements, verify=None, commit=False):
    """Виконує команди в транзакції; без commit транзакцію завжди скасовують."""
    if isinstance(statements, str):
        statements = [statements]
    out = Outcome()
    db.conn.execute("BEGIN")
    try:
        for sql in setup:
            try:
                db.conn.execute(sql)
            except psycopg.Error as error:
                raise RuntimeError(f"помилка підготовки тесту: {error}") from None
        try:
            for sql in statements:
                db.conn.execute(sql)
            if commit:
                db.conn.execute("COMMIT")
            if verify:
                out.value = db.value(verify)
        except psycopg.Error as error:
            out.state, out.constraint, out.column = error.sqlstate, error.diag.constraint_name, error.diag.column_name
            out.message = str(error).strip()
            found = re.search(r'column "(\w+)"', out.message)
            if out.state == "23502" and not out.column and found:
                out.column = found.group(1)
    finally:
        db.conn.execute("ROLLBACK")
    return out
