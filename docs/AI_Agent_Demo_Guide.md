# 🤖 Руководство по интеграции ИИ-агента (MCP)

В документе описано, как ИИ-агент (Zoo-code / Cline) используется для тестирования приложения **СОУИ**. Протокол **Model Context Protocol (MCP)** позволяет агенту напрямую обращаться к базе данных, анализировать схему и находить логические дефекты.

## 1. Интеграция MCP

Агент взаимодействует с PostgreSQL через локальный MCP-сервер.

* **Конфигурация:** Используется официальный сервер `@modelcontextprotocol/server-postgres` (настройки в `mcp/cline_mcp_settings.json`).
* **Доступ агента:**
  * Инспекция DDL-схемы (таблицы, связи, типы данных).
  * Выполнение Read-Only SQL-запросов для сверки ответов API с реальными данными в БД.
  * Валидация констрейнтов (`FOREIGN KEY`, `ON DELETE RESTRICT`, `CHECK`).

## 2. Системные промпты

Работа агента управляется инструкциями из папки [`.agent/prompts/`](../.agent/prompts/). Они задают строгий формат вывода и предотвращают "галлюцинации":

* [`01_test_designer.prompt.md`](../.agent/prompts/01_test_designer.prompt.md) — Проектирование тест-кейсов и матрицы покрытия.
* [`02_crud_testing.prompt.md`](../.agent/prompts/02_crud_testing.prompt.md) — Сквозное тестирование CRUD-операций REST API.
* [`03_field_validation.prompt.md`](../.agent/prompts/03_field_validation.prompt.md) — Граничный анализ (BVA) и попытки обхода `CHECK`-ограничений.
* [`04_reports_testing.prompt.md`](../.agent/prompts/04_reports_testing.prompt.md) — Сверка (reconciliation) данных API и результатов SQL-запросов.
* [`05_bug_reporter.prompt.md`](../.agent/prompts/05_bug_reporter.prompt.md) — Генерация баг-репортов по шаблону Jira (Markdown).

## 3. Воркфлоу тестирования

Процесс работы выстроен по шагам:

1. **Запуск:** Поднятие FastAPI и PostgreSQL через Docker Compose.
2. **Smoke-тест:** Базовый прогон API-тестов (Postman/Newman).
3. **AI-Анализ:** Агент через MCP читает схему БД и ищет расхождения с требованиями.
4. **Репортинг:** Автоматическое оформление найденных дефектов в баг-репорты.

## 4. Артефакты работы агента

Примеры реальных задач, выполненных агентом и сохраненных в репозитории:

* **Поиск дефекта в БД:** Агент проанализировал DDL-схему и нашел ошибку в регулярном выражении `student_group` (не принимает дефис в шифре 'ИВТ-21').
  👉 [BUG-001-group-code-hyphen-check.md](bug_reports/BUG-001-group-code-hyphen-check.md)
* **Комплексный QA-аудит:** Агент выполнил SQL-запросы, проверил каскадное удаление, составил матрицу покрытия и нашел логический баг с двойными фамилиями.
  👉 [AI_QA_Audit_Report.md](test-management/AI_QA_Audit_Report.md)