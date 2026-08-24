[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 🎓 СОУИ — QA Engineering Hub & AI Sandbox

Комплексный тестовый стенд и портфолио для **Системы Обработки Учебной Информации (СОУИ)**. Проект демонстрирует практики тестирования REST API, реляционных БД (PostgreSQL), тест-дизайна, а также интеграцию ИИ-агентов через Model Context Protocol (MCP).

---

## 🏗️ Архитектура системы

```mermaid
graph TD
    Client[Client / Postman / Swagger] --> API[FastAPI Backend]
    API --> DB[(PostgreSQL 16)]
    Agent[AI Agent / Zoo-code Gemini] --> MCP[Model Context Protocol]
    MCP --> DB
```

---

## 🛠️ Технологический стек

* **Backend / API**: Python 3.11, FastAPI, SQLAlchemy, Pydantic, Uvicorn
* **Database**: PostgreSQL 16 (с CHECK-ограничениями и ссылочной целостностью)
* **QA & Test Design**: [`Test Cases Suite`](docs/test-management/Test_Cases_Suite.md), ERD-диаграммы, MindMap
* **API Testing**: Postman Collection [`soui_postman_collection.json`](tests/soui_postman_collection.json), Newman CLI, Swagger / ReDoc
* **AI Integration**: Zoo-code (форк Roo-code) в GitHub Codespaces, Model Context Protocol [`cline_mcp_settings.json`](mcp/cline_mcp_settings.json), промпты в [`.agent/prompts/qa_analyst.prompt.md`](.agent/prompts/qa_analyst.prompt.md)
* **DevOps & CI/CD**: Docker, Docker Compose [`docker-compose.yml`](docker/docker-compose.yml), GitHub Actions [`.github/workflows/qa.yml`](.github/workflows/qa.yml)

---

## 🚀 Быстрый старт (Quick Start)

### Предварительные требования
* Docker Engine (20.10+) & Docker Compose (v2+)
* Свободные порты: `8000` (FastAPI) и `5432` (PostgreSQL)

### Запуск сервисов
```bash
# Копирование файла переменных окружения (при необходимости)
cp .env.example .env

# Запуск контейнеров
docker-compose -f docker/docker-compose.yml up --build -d
```

* **Swagger API**: `http://localhost:8000/docs`
* **ReDoc API**: `http://localhost:8000/redoc`
* **PostgreSQL**: `localhost:5432` (`soui_db` / `qa_admin` / `qa_secure_password`)

---

## 🤖 AI Integration & MCP

Подробное руководство по настройке и использованию ИИ-агента **Zoo-code (форк Roo-code)**, подключению к Google Gemini API и взаимодействию с базой данных через Model Context Protocol (MCP) описано в файле [`AI_INTEGRATION.md`](docs/AI_INTEGRATION.md).

* **ИИ-агент**: **Zoo-code (форк Roo-code)** в среде **GitHub Codespaces**.
* **LLM Engine**: Google Gemini API.
* **MCP Server**: [`postgres-soui`](mcp/cline_mcp_settings.json) для прямого доступа к схеме и данным PostgreSQL.
* **Промпты агента**: [`.agent/prompts/`](.agent/prompts/qa_analyst.prompt.md) (`qa_analyst.prompt.md`, `sql_validator.prompt.md`, `bug_reporter.prompt.md`).

---

## 🧪 Запуск тестов

### 1. SQL-валидация и проверки целостности
```bash
# Проверка CHECK-ограничений и целостности
docker exec -i soui_qa_db psql -U qa_admin -d soui_db < sql-tests/01_integrity_and_constraints.sql

# Сводный отчет успеваемости
docker exec -i soui_qa_db psql -U qa_admin -d soui_db < sql-tests/02_business_logic_reports.sql
```

### 2. API-тесты (Postman / Newman)
```bash
# Установка зависимостей (при необходимости)
npm install

# Запуск API-тестов через npm
npm run test:api

# Или напрямую через npx newman
npx newman run tests/soui_postman_collection.json --env-var "baseUrl=http://localhost:8000"
```

---

## 📂 Навигация по репозиторию

* [`app/`](app/main.py) — Исходный код FastAPI бэкенда и моделей БД.
* [`docker/`](docker/docker-compose.yml) — Конфигурация Docker (`docker-compose.yml`) и скрипты инициализации БД (`01_schema.sql`, `02_seed_data.sql`).
* [`docs/`](docs/AI_INTEGRATION.md) — Документация по проекту: [`AI_INTEGRATION.md`](docs/AI_INTEGRATION.md), [`AI_Agent_Demo_Guide.md`](docs/AI_Agent_Demo_Guide.md), тест-кейсы ([`Test_Cases_Suite.md`](docs/test-management/Test_Cases_Suite.md)), ERD-диаграммы (`erd_schema_soui.jpg`) и MindMap (`mindmap_soui.jpg`).
* [`sql-tests/`](sql-tests/01_integrity_and_constraints.sql) — SQL-скрипты проверки бизнес-логики и ограничений.
* [`tests/`](tests/soui_postman_collection.json) — Коллекция Postman для тестирования API.
* [`.agent/`](.agent/prompts/qa_analyst.prompt.md) — Промпты для AI QA-агента Zoo-code и конфигурация MCP [`cline_mcp_settings.json`](mcp/cline_mcp_settings.json).
* [`.github/workflows/`](.github/workflows/qa.yml) — Пайплайн автоматизированного тестирования в GitHub Actions CI/CD.

---

## 👤 Автор

* **QA Engineer**: Станислав Меховский ([@stasmeh](https://github.com/stasmeh))
* **Репозиторий**: [soui-qa-automation-hub](https://github.com/stasmeh/soui-qa-automation-hub)
