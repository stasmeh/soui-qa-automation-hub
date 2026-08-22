# 🎓 СОУИ — QA Automation & Test Engineering Hub

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
