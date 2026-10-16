# Стартовий проєкт OBDZ-P03

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace): конфігурація `.devcontainer` сама підніме контейнер із Python і контейнер із сервером PostgreSQL 18, а змінні `PGHOST`, `PGUSER`, `PGPASSWORD` буде задано. Локально: запустіть PostgreSQL 18 командою `docker run --name obdz-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:18`, потім `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`. Якщо порт 5432 зайнятий, змініть його в команді `docker run` і задайте змінну `PGPORT`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Відкрийте файл `variants/variant_NN.py` своєї задачі, впишіть номер варіанта в константу `VARIANT` і реалізуйте функцію за карткою.
3. Запускайте відкриті тести своєї задачі: `pytest tests/test_variants.py -k TNN` (NN з двома цифрами). Тести інших наборів даних пропускаються. Для PostgreSQL права адміністратора на вашому комп'ютері не потрібні.
4. Щоб побачити, що створив ваш скрипт, виконайте `python run_my.py`: він запускає скрипт у тимчасовій схемі й друкує таблиці, стовпці та обмеження, а для задач 9 і 10 ще й діагностику помилок та результат `drop_script()`.
5. Змінюйте лише свій файл у `variants/` і файл `tests/test_my.py` (власні перевірки, створіть його самі). Файли в `tests/` (крім `test_my.py`) і `data/` не змінюйте.
6. Файли `data/t07_setN.sql` і `data/t09_setN.sql` містять початкові стани для задач 7 і 9; тест створює їх сам, ці файли потрібні лише для читання.
7. Підсумок для здачі: файл `variants/variant_NN.py`, `tests/test_my.py`, `ANSWERS.md` і знімок екрана (розділ 10 завдання).
