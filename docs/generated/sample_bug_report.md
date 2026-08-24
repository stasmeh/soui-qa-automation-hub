# 🐛 Пример баг-репорта (сгенерирован ИИ-агентом Zoo-code)

1. **Summary:** [Журнал успеваемости] Возможна вставка отрицательной оценки при некорректной настройке ограничений
2. **Issue Type:** Bug
3. **Environment:** PostgreSQL 16 (Docker), FastAPI Backend, GitHub Codespaces (Linux 6.8)
4. **Severity / Priority:** Major / High — Нарушение бизнес-логики учета оценок студентов.
5. **Preconditions:**
   - Выполнен запуск Docker Compose сервисов.
   - База данных содержит записи в `teacher`, `student`, `control_point`, `assignment`.
6. **Steps to Reproduce:**
   1. Подключиться к БД через MCP-сервер `postgres-soui`.
   2. Выполнить SQL-запрос:
      ```sql
      INSERT INTO journal (teacher_id, student_id, control_point_id, assignment_id, grade, submission_date)
      VALUES (1, 1, 1, 1, -10, '2026-05-15');
      ```
7. **Expected Result:** СУБД отклоняет запись с ошибкой `CHECK constraint violation (grade BETWEEN 0 AND 60)`.
8. **Actual Result:** При наличии ограничения `CHECK (grade >= 0 AND grade <= 60)` запись успешно отклоняется. (Тест пройден).
9. **Attachments / Logs:**
   ```
   ERROR: new row for relation "journal" violates check constraint "journal_grade_check"
   DETAIL: Failing row contains (1, 1, 1, 1, 1, -10, 2026-05-15).
   ```
10. **Workaround:** Отсутствует (требуется соблюдение ограничений целостности БД).
