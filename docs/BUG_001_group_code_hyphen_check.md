# Отчет об ошибке: BUG-001

- **Title (Заголовок):** [DB Schema] Ошибка валидации CHECK-ограничения шифра группы с дефисом при инициализации базы данных в [01_schema.sql](../docker/init-db/01_schema.sql)
- **Severity / Priority:** Blocker / High (Блокирует развертывание приложения и инициализацию сид-данных)
- **Environment:** Docker Compose, FastAPI, PostgreSQL 16 (контейнеры `soui_qa_db` и `soui_web_service` из [docker-compose.yml](../docker/docker-compose.yml))
- **Preconditions (Предусловия):** Запуск сервисов через `docker compose up -d` с чистым томом базы данных [docker-compose.yml](../docker/docker-compose.yml).
- **Steps to Reproduce (Шаги для воспроизведения):**
  1. Выполнить команду `docker compose -f docker/docker-compose.yml down -v && docker compose -f docker/docker-compose.yml up -d`.
  2. Проверить логи контейнера PostgreSQL `docker compose logs postgres-db`.
  3. Выполнить HTTP-запрос `GET /api/v1/groups?sort_by_name=true` через `curl` или обратиться к [main.py](../app/main.py).
- **Actual Result (Фактический результат):** 
  - Ошибка в логах БД: `ERROR: new row for relation "student_group" violates check constraint "student_group_group_code_check"`, деталь: `Failing row contains (1, Информатика и ВТ, ИВТ-21, 1)` при выполнении скрипта [02_seed_data.sql](../docker/init-db/02_seed_data.sql).
  - Таблицы остаются пустыми, эндпоинт [main.py](../app/main.py) возвращает пустой массив `[]`.
- **Expected Result (Ожидаемый результат):** 
  - Успешное выполнение скрипта инициализации [02_seed_data.sql](../docker/init-db/02_seed_data.sql) со всеми тестовыми данными.
  - Шифры учебных групп, содержащие дефисы (например, `'ИВТ-21'`), должны успешно проходить проверку целостности.
- **Root Cause Analysis (Предполагаемая причина):** В файле [01_schema.sql](../docker/init-db/01_schema.sql) регулярное выражение для проверки `group_code` задано как `CHECK (group_code ~ '^[А-Яа-яЁё0-9\s]+$')`, в котором отсутствует символ дефиса (`-`), необходимый для стандартных академических шифров групп.
