[![QA Automation Pipeline](https://github.com/stasmeh/soui-qa-automation-hub/actions/workflows/qa.yml/badge.svg)](https://github.com/stasmeh/soui-qa-automation-hub/actions/workflows/qa.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
![AI-Driven](https://img.shields.io/badge/AI_Agent-Zoo--code%20%7C%20Gemini-8A2BE2?style=flat&logo=openai&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Protocol-FF4500?style=flat)


# 🎓 SOUI — QA Automation & AI-Driven Testing Hub

SOUI — это учебно-демонстрационный стенд (QA-песочница) журнала учета успеваемости. В логику приложения и структуру БД намеренно заложены дефекты. Это сделано специально, чтобы продемонстрировать, как AI-агент (через MCP) может анализировать архитектуру, находить расхождения с требованиями и автоматически составлять баг-репорты.

## 🎯 Ключевые особенности проекта

* **QA-песочница (FastAPI):** REST API с намеренно заложенными дефектами логики для практики поиска багов.
* **Тестирование БД (PostgreSQL):** Проверка целостности данных, бизнес-ограничений (`CHECK`, `FK`) и работы транзакций.
* **🤖 AI-агент через MCP:** ИИ (Zoo-code / Cline + Gemini) самостоятельно анализирует структуру БД, выполняет проверки (BVA) и автоматически генерирует баг-репорты.
* **Docs-as-Code:** Тест-кейсы и баг-репорты ведутся в формате Markdown прямо в репозитории.
* **Автотесты API:** Написаны коллекции проверок для запуска через Postman + Newman.

---

## 🏗️ Архитектура и интеграция ИИ

```mermaid
graph TD
    %% Определение узлов
    Client("Client<br/>(Postman / Newman / CLI)")
    API("API<br/>(FastAPI Backend)")
    DB[("Database<br/>(PostgreSQL 16)")]
    
    LLM(("Gemini AI"))
    Agent("Agent<br/>(Zoo-code)")
    MCP("MCP Server<br/>(postgres-soui)")

    %% Определение связей (всё сходится к единой БД)
    Client -->|HTTP / REST| API
    API -->|SQL / ORM| DB
    
    LLM -. API Key .-> Agent
    Agent -->|MCP Protocol| MCP
    MCP -->|SQL Tests / Checks| DB

    %% Стилизация узлов (мягкие цвета для лучшей читаемости)
    style Client fill:#f8f9fa,stroke:#ced4da,stroke-width:2px,color:#212529
    style API fill:#d1e7dd,stroke:#198754,stroke-width:2px,color:#212529
    style DB fill:#cfe2ff,stroke:#0d6efd,stroke-width:2px,color:#212529
    
    style LLM fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,color:#212529
    style Agent fill:#e0cffc,stroke:#8a2be2,stroke-width:2px,color:#212529
    style MCP fill:#ffe69c,stroke:#ff8c00,stroke-width:2px,color:#212529
```

## 🛠 Стек технологий

* **Backend:** FastAPI, Python, Pydantic
* **Database:** PostgreSQL 16
* **QA & Automation:** Postman, Newman, SQL-скрипты, Docker, Docker Compose
* **AI Integration:** Zoo-code (Cline fork), Gemini API, MCP-сервер (postgres-soui)

---

## 📂 Структура репозитория
```text
.
├── app/                  # Исходный код FastAPI сервиса (models, database)
├── docker/               # Инфраструктура: docker-compose и SQL-скрипты миграций
├── docs/                 # QA-документация:
│   ├── bug_reports/      #   Оформленные баг-репорты 
│   ├── diagrams/         #   Mermaid-схемы и ERD-диаграммы базы данных
│   └── test-management/  #   Тест-кейсы и отчёты о тестировании (QA_Checklist.md)
├── mcp/                  # Конфигурация Model Context Protocol для подключения агента
├── sql-tests/            # SQL-скрипты: проверка констрейнтов и целостности данных
├── tests/                # Коллекции Postman для автотестов API
└── .agent/prompts/       # (Скрытая директория) Промпты для AI-агента
```

---

## 🚀 Быстрый старт

Проект разворачивается локально с помощью Docker. Предварительно убедитесь, что у вас установлены Docker и Node.js (для тестов):

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

1. **Анализ схемы БД:** Агент запрашивает структуру таблиц и выявляет расхождения с требованиями (например, неверные регулярные выражения в `CHECK`).
2. **Генерация проверок:** Создает чек-листы и SQL-тесты на основе структуры таблиц (`02_crud_testing.prompt.md`).
3. **Оформление багов:** Анализирует ошибки СУБД (например, нарушение CHECK constraint) и оформляет структурированные баг-репорты по Jira-шаблону (`05_bug_reporter.prompt.md`).

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

## Источники

Промты для AI-агента в директории `.agent/prompts/` основаны на материалах из репозитория
[QA Prompt Library](https://github.com/tayyabakmal1/qa-prompt-library) (автор: Tayyab Akmal).
Оригинальные промты были адаптированы и модифицированы под контекст проекта SOUI.
Лицензия: MIT.