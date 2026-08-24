# 🤖 Руководство по интеграции ИИ-агентов и MCP (AI-Driven QA Guide)

В данном документе описана архитектура и практический процесс использования ИИ-агентов в роли QA-инженеров для тестирования системы **СОУИ (Система Обработки Учебной Информации)** с помощью протокола **Model Context Protocol (MCP)**.

---

## 🛠️ 1. Интеграция Model Context Protocol (MCP)

ИИ-агент взаимодействует с базой данных через выделенный MCP-сервер `postgres-soui`.
* **Конфигурация:** Настройки подключения и запуска сервера определены в файле [`mcp/cline_mcp_settings.json`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/mcp/cline_mcp_settings.json).
* **Возможности через MCP:**
  * Прямая инспекция схемы базы данных PostgreSQL 16 (таблицы, колонки, типы данных).
  * Выполнение read-only SQL-запросов для анализа текущего состояния данных.
  * Валидация ограничений целостности, внешних ключей (`FK`) и `CHECK`-ограничений.

---

## 📋 2. Системные промпты агента (`.agent/prompts/`)

1. [`01_test_designer.prompt.md`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/.agent/prompts/01_test_designer.prompt.md) — Проектирование тест-кейсов и построение матрицы покрытия требований.
2. [`02_crud_testing.prompt.md`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/.agent/prompts/02_crud_testing.prompt.md) — Методология и чек-листы для сквозного тестирования CRUD-операций REST API.
3. [`03_field_validation.prompt.md`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/.agent/prompts/03_field_validation.prompt.md) — Анализ граничных значений (BVA) и валидация полей ввода данных.
4. [`04_reports_testing.prompt.md`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/.agent/prompts/04_reports_testing.prompt.md) — Проверка аналитических отчетов и корректности агрегирующих SQL-запросов.
5. [`05_bug_reporter.prompt.md`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/.agent/prompts/05_bug_reporter.prompt.md) — Автоматическая генерация формализованных баг-репортов в стандарте Jira на основе логов ошибок сервера и БД.

---

## 🔄 3. Основной воркфлоу QA-агента

Процесс работы с ИИ-помощником состоит из следующих последовательных шагов:

* **Шаг 1: Запуск окружения**
  Развертывание инфраструктуры (FastAPI и PostgreSQL 16) с помощью Docker Compose ([`docker-compose.yml`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/docker/docker-compose.yml)).
* **Шаг 2: Выполнение базовых тестов**
  Запуск автотестов API через Postman/Newman ([`tests/soui_postman_collection.json`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/tests/soui_postman_collection.json)) и SQL-проверок целостности ([`sql-tests/01_integrity_and_constraints.sql`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/sql-tests/01_integrity_and_constraints.sql)).
* **Шаг 3: Инспекция схемы через MCP**
  Подключение агента к базе данных `soui_db` через сервер `postgres-soui` для анализа структуры данных и выявления расхождений с требованиями.
* **Шаг 4: Синтез результатов и оформление дефектов**
  Генерация отчетов и фиксация обнаруженных несоответствий в виде детальных баг-репортов (например, [`BUG_001_group_code_hyphen_check.md`](https://github.com/stasmeh/soui-qa-automation-hub/blob/main/docs/bug_reports/BUG_001_group_code_hyphen_check.md)).
