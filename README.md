[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
![AI-Driven](https://img.shields.io/badge/AI_Agent-Zoo--code%20%7C%20Gemini-8A2BE2?style=flat&logo=openai&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Protocol-FF4500?style=flat)

# 🎓 SOUI — QA Automation & AI-Driven Testing Hub

Практический тестовый стенд на базе **Системы Обработки Учебной Информации (СОУИ)**. Проект разработан для демонстрации навыков автоматизации тестирования, продвинутого SQL и интеграции ИИ-агентов в реальный QA-процесс.

## 🎯 Ключевые особенности проекта
1. **Тестирование Backend & DB:** Проверка REST API (FastAPI) и глубокая валидация СУБД (PostgreSQL 16) на уровне `CHECK`-ограничений, `FOREIGN KEY` (ON DELETE RESTRICT) и транзакций.
2. **AI-Driven QA via MCP:** Уникальная интеграция ИИ-агента через **Model Context Protocol (MCP)**. Агент напрямую анализирует схему базы данных, выполняет граничный анализ (BVA) и автоматически генерирует формализованные баг-репорты.
3. **Docs-as-Code:** Архитектура, тест-кейсы и баг-репорты ведутся в Markdown прямо в репозитории.

---

## 🏗️ Архитектура и интеграция ИИ

```mermaid
graph TD
    Client[Postman / Newman / CLI] --> API[FastAPI Backend]
    API --> DB[(PostgreSQL 16)]
    Agent[AI Agent / Zoo-code] --> MCP[MCP Server: postgres-soui]
    MCP --> DB
    style Agent fill:#8A2BE2,color:#fff
    style MCP fill:#FF4500,color:#fff
```

## 📂 Структура репозитория
```text
.
.
├── app/                  # Исходный код FastAPI сервиса (models, database)
├── docker/               # Инфраструктура: docker-compose и SQL-скрипты миграций
├── docs/                 # QA-документация:
│   ├── bug_reports/      #   Оформленные баг-репорты (например, BUG_001)
│   ├── diagrams/         #   Mermaid-схемы и ERD-диаграммы базы данных
│   ├── generated/        #   Сырые артефакты от ИИ-агента (ревью перед оформлением)
│   └── test-management/  #   Тест-кейсы и тест-планы (Test_Cases_Suite.md)
├── mcp/                  # Конфигурация Model Context Protocol для подключения агента
├── sql-tests/            # Сложные SQL-запросы: проверка констрейнтов и бизнес-логики
├── tests/                # Коллекции Postman для автотестов API
└── .agent/prompts/       # (Скрытая директория) Системные промпты для AI-агента
```

---

## 🚀 Быстрый старт

Запуск проекта выполняется в одну команду с помощью Docker Compose:

```bash
git clone https://github.com/stasmeh/soui-qa-automation-hub.git
cd soui-qa-automation-hub
docker compose -f docker/docker-compose.yml up --build -d
```

* **Swagger UI (FastAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **PostgreSQL:** `localhost:5432` (User: `qa_admin`, DB: `soui_db`)

---

## 🤖 Как работает ИИ-агент (AI-Assisted QA)

ИИ-агент (`Zoo-code` / `Cline`) подключается к PostgreSQL через `postgres-soui` сервер и выполняет задачи по заготовленным промптам (директория [`.agent/prompts/`](.agent/prompts/)):

1. **Инспекция БД:** Агент запрашивает схему данных и находит расхождения требований (например, неверные регулярные выражения в `CHECK`).
2. **Генерация проверок:** Создает чек-листы и SQL-тесты на основе структуры таблиц (`02_crud_testing.prompt.md`).
3. **Оформление багов:** Автоматически парсит ошибки (например, `violates check constraint`) и переводит их в стандартные баг-репорты Jira-формата (`05_bug_reporter.prompt.md`).

Подробное руководство по настройке агента: [`AI_Agent_Demo_Guide.md`](docs/AI_Agent_Demo_Guide.md).

---

## 🧪 Запуск тестов

1. **API-автотесты (Postman + Newman):**
   ```bash
   npm install
   npm run test:api
   ```

2. **Интеграционные SQL-тесты целостности БД:**
   ```bash
   docker exec -i soui_qa_db psql -U qa_admin -d soui_db < sql-tests/01_integrity_and_constraints.sql
   ```

---

## 👤 Автор

Станислав Меховский | QA Engineer

* GitHub: [@stasmeh](https://github.com/stasmeh)
* Telegram: [marselle2021](https://t.me/marselle2021)