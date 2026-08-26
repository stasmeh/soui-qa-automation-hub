# Отчет об ошибке: BUG-002

- **Title (Заголовок):** [DB Schema] Ошибка валидации CHECK-ограничения `student_last_name_check` при вставке студента со сложной фамилией через дефис в [01_schema.sql](../../docker/init-db/01_schema.sql)
- **Severity / Priority:** Major / Medium (Препятствует добавлению в систему студентов со сложными/двойными фамилиями, содержащими дефис)
- **Environment:** Docker Compose, FastAPI, PostgreSQL 16 (контейнеры `soui_qa_db` и `soui_web_service` из [docker-compose.yml](../../docker/docker-compose.yml))
- **Preconditions (Предусловия):** 
  1. База данных развернута и инициализирована через [docker-compose.yml](../../docker/docker-compose.yml).
  2. В таблице `student_group` существует группа с `group_id = 1`.
- **Steps to Reproduce (Шаги для воспроизведения):**
  1. Подключиться к базе данных PostgreSQL `soui_db` под пользователем `qa_admin`.
  2. Выполнить SQL-запрос INSERT в таблицу `student`:
     ```sql
     INSERT INTO student (last_name, first_name, middle_name, group_id, student_card_number, education_form) 
     VALUES ('Иванов-Петров', 'Иван', 'Иванович', 1, 901002, 'бюджетное');
     ```
- **Actual Result (Фактический результат):**
  - Запрос завершается с ошибкой нарушения CHECK-ограничения `student_last_name_check`:
    `ERROR: new row for relation "student" violates check constraint "student_last_name_check"`
    `DETAIL: Failing row contains (7, Иванов-Петров, Иван, Иванович, 901002, бюджетное, 1).`
  - Запись о студенте не добавляется в таблицу `student`.
- **Expected Result (Ожидаемый результат):**
  - Запись с двойной/сложной фамилией, содержащей дефис (например, `'Иванов-Петров'`), успешно вставляется в таблицу `student`.
- **Root Cause Analysis (Предполагаемая причина):** 
  - В файле DDL-схемы [01_schema.sql](../../docker/init-db/01_schema.sql) ограничение таблицы `student` определено как:
    `last_name VARCHAR(100) NOT NULL CHECK (last_name ~ '^[А-Яа-яЁё]+$')`
  - Регулярное выражение `^[А-Яа-яЁё]+$` допускает только буквы кириллицы и не содержит символ дефиса (`\-` или `-`), из-за чего валидация для фамилий с дефисом ("Иванов-Петров", "Мамин-Сибиряк" и т.д.) завершается ошибкой. Требуется исправить regex на `^[А-Яа-яЁё\-]+$` или `^[А-Яа-яЁё\s\-]+$`.
