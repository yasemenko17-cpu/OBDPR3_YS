"""Виконує ваш скрипт у тимчасовій схемі PostgreSQL і показує, що створено.

Використання:  python run_my.py [номер_задачі]
Без аргумента обробляються всі файли variants/variant_NN.py, де задано VARIANT. Після виконання схема видаляється.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tests"))

import pgutil  # noqa: E402
from conftest import load  # noqa: E402
from specs import SPECS  # noqa: E402


def summary(db):
    for table in pgutil.tables(db):
        print(f"  таблиця {table}")
        for name, c in pgutil.columns(db, table).items():
            flags = [x for x in (
                "NOT NULL" if c["notnull"] else "", {"a": "IDENTITY ALWAYS", "d": "IDENTITY BY DEFAULT"}.get(c["identity"], ""),
                {"s": "GENERATED STORED", "v": "GENERATED VIRTUAL"}.get(c["generated"], ""),
                f"DEFAULT {c['default']}" if c["default"] and not c["generated"] else "") if x]
            print(f"    {name:<18} {c['type']:<28} {' '.join(flags)}")
        for k in pgutil.constraints(db, table):
            print(f"    [{k['type']}] {k['name']}: {k['def']}")


def run(task):
    module = load(task)
    variant = getattr(module, "VARIANT", 0)
    if not variant:
        print(f"Задача {task}: VARIANT не задано, пропущено")
        return
    set_no = (variant - 1) % 3 + 1
    spec = SPECS.get((task, set_no))
    print(f"=== Задача {task}, варіант {variant} (набір {set_no}) ===")
    db = pgutil.Db()
    try:
        if spec and spec.get("setup"):
            db.run(spec["setup"])
        if task == 9:
            for i, sql in enumerate(module.violations(), 1):
                out = pgutil.attempt(db, [], sql)
                where = out.constraint or out.column or "-"
                print(f"  {i}. {out.state or 'без помилки'} ({where}): {out.message.splitlines()[0] if out.message else ''}")
            return
        if task == 10:
            db.run(module.create_script())
            summary(db)
            db.run(module.drop_script())
            print(f"  після drop_script() таблиць у схемі: {len(pgutil.tables(db))}")
            return
        db.run(module.script())
        summary(db)
    except pgutil.ScriptError as error:
        print("  Помилка SQL:", error)
    except NotImplementedError:
        print("  Функцію ще не реалізовано (NotImplementedError)")
    finally:
        db.close()


if __name__ == "__main__":
    for number in ([int(sys.argv[1])] if len(sys.argv) > 1 else range(1, 11)):
        run(number)
