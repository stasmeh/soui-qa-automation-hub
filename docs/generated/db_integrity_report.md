# 📊 Отчет о проверке целостности БД (сгенерирован ИИ-агентом Zoo-code)

**Дата проверки:** 2026-08-24  
**СУБД:** PostgreSQL 16.0 (Alpine)  
**Инструмент проведения:** Zoo-code Agent + MCP (`postgres-soui`)  

---

## 🔍 Результаты выполнения валидационных скриптов

### 1. Ограничения `CHECK` ([`sql-tests/01_integrity_and_constraints.sql`](../../sql-tests/01_integrity_and_constraints.sql))

| № | Проверяемое условие | Выполненный запрос / Попытка | Результат | Статус |
|---|---------------------|-----------------------------|-----------|--------|
| 1 | `grade BETWEEN 0 AND 60` | `INSERT INTO journal ... grade = 75` | `ERROR: violates check constraint "journal_grade_check"` | PASS ✅ |
| 2 | Кириллица в ФИО | `INSERT INTO student ... last_name = 'Smith'` | `ERROR: violates check constraint "student_last_name_check"` | PASS ✅ |
| 3 | `ON DELETE RESTRICT` | `DELETE FROM specialty WHERE specialty_id = 1` | `ERROR: violates foreign key constraint` | PASS ✅ |

---

## 📌 Выводы
Все ограничения схемы базы данных `soui_db` настроены корректно и соответствуют требованиям спецификации ТЗ.
