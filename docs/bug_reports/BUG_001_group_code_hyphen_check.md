# Отчет об ошибке: BUG-001

- **Title (Заголовок):** [DB Schema] Ошибка валидации CHECK-ограничения шифра группы с дефисом при инициализации базы данных в [`docker/init-db/01_schema.sql`](docker/init-db/01_schema.sql:10)
- **Severity / Priority:** Blocker / High (Блокирует развертывание приложения и инициализацию сид-данных)
- **Environment:** Docker Compose, FastAPI, PostgreSQL 16 (контейнеры `soui_qa_db` и `soui_web_service` из [`docker/docker-compose.yml`](docker/docker-compose.yml:1))
- **Preconditions (Предусловия):** Запуск сервисов через `docker compose up -d` с чистым томом базы данных [`docker/docker-compose.yml`](docker/docker-compose.yml:4).
- **Steps to Reproduce (Шаги для воспроизведения):**
  1. Выполнить команду `docker compose -f docker/docker-compose.yml down -v && docker compose -f docker/docker-compose.yml up -d`.
  2. Проверить логи контейнера PostgreSQL `docker compose logs postgres-db`.
  3. Выполнить HTTP-запрос `GET /api/v1/groups?sort_by_name=true` через `curl` или обратиться к [`app/main.py`](app/main.py:272).
- **Actual Result (Фактический результат):** 
  - Ошибка в логах БД: `ERROR: new row for relation "student_group" violates check constraint "student_group_group_code_check"`, деталь: `Failing row contains (1, Информатика и ВТ, ИВТ-21, 1)` при выполнении скрипта [`docker/init-db/02_seed_data.sql`](docker/init-db/02_seed_data.sql:2).
  - Таблицы остаются пустыми, эндпоинт [`app/main.py`](app/main.py:272) возвращает пустой массив `[]`.
- **Expected Result (Ожидаемый результат):** 
  - Успешное выполнение скрипта инициализации [`docker/init-db/02_seed_data.sql`](docker/init-db/02_seed_data.sql:2) со всеми тестовыми данными.
  - Шифры учебных групп, содержащие дефисы (например, `'ИВТ-21'`), должны успешно проходить проверку целостности.
- **Root Cause Analysis (Предполагаемая причина):** В файле [`docker/init-db/01_schema.sql`](docker/init-db/01_schema.sql:10) регулярное выражение для проверки `group_code` задано как `CHECK (group_code ~ '^[А-Яа-яЁё0-9\s]+$')`, в котором отсутствует символ дефиса (`-`), необходимый для стандартных академических шифров групп.
