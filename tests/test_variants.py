"""Відкриті тести вашого варіанта (решта наборів пропускається за константою VARIANT). Ідентифікатор тесту: T<задача>-S<набір>-<перевірка>.

Запуск повного набору: pytest. Одна задача: pytest -k T05. Один набір: pytest -k "T05-S2".
"""
import pytest
from checks import run_case
from conftest import load
from specs import SPECS

CASES = [(t, s, chk) for (t, s), spec in sorted(SPECS.items()) for chk in spec["checks"]]


@pytest.mark.parametrize("task,set_no,check", CASES, ids=[f"T{t:02d}-S{s}-{c['id']}" for t, s, c in CASES])
def test_check(db, task, set_no, check):
    run_case(db, load(task), task, set_no, SPECS[(task, set_no)], check)
