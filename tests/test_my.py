from conftest import load
from pgutil import attempt

def test_my_priority_check(db):
    module = load(8)
    db.run(module.script())
    # Перевірка порушення CHECK на пріоритет (значення поза діапазоном 1-10)
    out = attempt(db, [], "INSERT INTO product VALUES (1, 'Телевізор'); INSERT INTO tag VALUES (1, 'Акція'); INSERT INTO product_tag VALUES (1, 1, 15);")
    assert out.state == "23514"
    assert out.constraint == "ck_pt_priority"

def test_my_category_self_check(db):
    module = load(8)
    db.run(module.script())
    # Перевірка самопосилання в категорії (parent_id не може дорівнювати id)
    out = attempt(db, [], "INSERT INTO category VALUES (1, 'Електроніка', 1);")
    assert out.state == "23514"
    assert out.constraint == "ck_category_not_self"

def test_my_cascade_delete(db):
    module = load(8)
    db.run(module.script())
    # Перевірка каскадного видалення у зв'язку багато-до-багатьох
    out = attempt(db, [], "INSERT INTO product VALUES (1, 'Телефон'); INSERT INTO tag VALUES (1, 'Новинка'); INSERT INTO product_tag VALUES (1, 1, 5); DELETE FROM product WHERE id = 1;")
    assert out.success == True