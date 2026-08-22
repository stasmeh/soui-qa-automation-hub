Markdown# 🎓 СОУИ — QA Automation & Test Engineering Hub

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16--alpine-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11--slim-3776AB.svg?logo=python&logoColor=white)](https://www.python.org)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-Postgres-8A2BE2.svg)](https://modelcontextprotocol.io)

Комплексный стенд тестирования и автоматизации для **Системы обработки учебной информации (СОУИ)**. Репозиторий содержит полнофункциональный бэкенд на FastAPI, реляционную СУБД PostgreSQL с контролем целостности, набор тест-кейсов, артефакты сниффинга трафика и конфигурацию AI-агентов через Model Context Protocol (MCP).

---

## 🏛 Архитектура и структура проекта

```text
soui-qa-automation-hub/
├── .agent/prompts/             # AI QA Agent Skills & System Prompts
├── app/                        # REST API Backend (FastAPI, SQLAlchemy, Pydantic)
│   ├── main.py                 # 8 CRUD сущностей, Swagger UI, фильтрация
│   ├── models.py               # ORM-модели базы данных
│   └── database.py             # Пул подключений PostgreSQL
├── docker/                     # Конфигурация контейнеризации
│   ├── docker-compose.yml      # Мультиконтейнерная сборка
│   └── init-db/                # DDL-схемы и сид-данные
├── docs/                       # Тестовая документация и диаграммы
│   ├── test-management/        # Матрица тест-кейсов (Test Suite)
│   └── diagrams/               # ERD и MindMap архитектуры
├── mcp/                        # Конфигурация Model Context Protocol
└── sql-tests/                  # SQL-скрипты валидации ограничений и отчетов
🧪 Охват тестирования (Test Scope)Уровень тестированияПроверяемая логикаИнструменты / СтекDatabase IntegrityОграничения CHECK (оценки 0–60, часы > 0), UNIQUE, ON DELETE RESTRICTPostgreSQL, DDL, Raw SQLREST API TestingПолный жизненный цикл 8 сущностей (CRUD), статус-коды 200/201/400/404/409FastAPI, Swagger/OpenAPI, PostmanBusiness LogicРежим преподавателя «Работа», сводная ведомость с агрегациями (AVG, COUNT)SQLAlchemy, SQL Group ByTraffic & SecurityПодмена тела запросов, обход валидации интерфейса, граничные датыCharles Proxy, Fiddler, DevToolsAI QA AutomationАвтономная верификация БД и генерация баг-репортовRoo Code / Cline, Gemini, MCP🚀 Быстрый старт стенда1. Локальный запуск через Docker ComposeBash# Клонирование репозитория
git clone [https://github.com/stasmeh/soui-qa-automation-hub.git](https://github.com/stasmeh/soui-qa-automation-hub.git)
cd soui-qa-automation-hub/docker

# Запуск базы данных и API
docker compose up --build -d
2. Доступ к интерактивной документацииSwagger UI: http://localhost:8000/docsReDoc: http://localhost:8000/redocPostgreSQL: localhost:5432 (soui_db, user: qa_admin, pass: qa_secure_password)🤖 Интеграция с AI-агентами (Model Context Protocol)В проект встроена конфигурация MCP-сервера базы данных PostgreSQL (mcp/cline_mcp_settings.json), позволяющая LLM-агентам автономно исследовать структуру таблиц, выполнять тестовые SQL-запросы и генерировать отчеты о дефектах по промптам из папки .agent/prompts/.
---

### Шаг 2. Отправка `README.md` на GitHub

В терминале PowerShell в папке `soui-qa-hub` выполните:

```powershell
git add README.md
git commit -m "docs: add comprehensive project README and architecture overview"
git push
