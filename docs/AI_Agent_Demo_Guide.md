# 🤖 AI Agent & MCP Integration Demo Guide

Данное руководство описывает концепцию и порядок использования ИИ-агентов (AI QA Engineers) с проектом **СОУИ (Система Обработки Учебной Информации)** через протокол **Model Context Protocol (MCP)**.

---

## 🛠️ Компоненты интеграции

1. **MCP Сервер (`server-postgres`)**:
   * Позволяет ИИ-агенту подключаться напрямую к базе данных PostgreSQL `soui_db`.
   * Конфигурация находится в файле [`mcp/cline_mcp_settings.json`](../mcp/cline_mcp_settings.json).

2. **Специализированные промпты агентов (`.agent/prompts/`)**:
   * [`qa_analyst.prompt.md`](../.agent/prompts/qa_analyst.prompt.md): Инструкции для QA Lead по тест-дизайну и планированию.
   * [`sql_validator.prompt.md`](../.agent/prompts/sql_validator.prompt.md): Инструкции для QA Database Automation Engineer по валидации ограничений БД.
   * [`bug_reporter.prompt.md`](../.agent/prompts/bug_reporter.prompt.md): Инструкции по генерации баг-репортов стандарта Jira.

---

## 🚀 Сценарии работы ИИ-агента

### Сценарий 1: Автоматическая проверка целостности БД
1. Агент подключается к БД через MCP-сервер `postgres-soui`.
2. Анализирует схемы и ограничения `CHECK`.
3. Выполняет проверочные SQL-запросы из [`sql-tests/01_integrity_and_constraints.sql`](../sql-tests/01_integrity_and_constraints.sql).
4. Генерирует отчет об обнаруженных несоответствиях.

### Сценарий 2: Генерация тест-кейсов и баг-репортов
1. Агент загружает требования и Mind Map из [`docs/diagrams/mindmap_soui.jpg`](./diagrams/mindmap_soui.jpg).
2. Сверяет фактическое поведение API с тест-кейсами из [`docs/test-management/Test_Cases_Suite.md`](./test-management/Test_Cases_Suite.md).
3. При обнаружении ошибок формирует структурированный баг-репорт.
