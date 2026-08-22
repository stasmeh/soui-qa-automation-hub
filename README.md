# 🎓 СОУИ — QA Automation & Test Engineering Hub

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Model Context Protocol](https://img.shields.io/badge/MCP-PostgreSQL-8A2BE2?style=flat-square)](https://modelcontextprotocol.io)

Тестовый стенд и комплекс обеспечения качества для **Системы обработки учебной информации (СОУИ)**. Репозиторий включает бэкенд на FastAPI, реляционную СУБД PostgreSQL с контролем целостности данных, набор тестовых сценариев, артефакты сниффинга трафика и интеграцию AI-агентов через Model Context Protocol (MCP).

---

## 📌 Архитектура проекта

```text
soui-qa-automation-hub/
├── .agent/prompts/             # Промпты и скиллы для AI QA-агента
├── app/                        # REST API бэкенд на FastAPI
│   ├── database.py             # Подключение к PostgreSQL (SQLAlchemy)
│   ├── main.py                 # Реализация эндпоинтов 8 сущностей
│   ├── models.py               # ORM-модели таблиц
│   └── requirements.txt        # Зависимости Python
├── docker/                     # Контейнеризация сервиса и БД
│   ├── docker-compose.yml      # Оркестрация контейнеров
│   └── init-db/                # DDL схемы и сид-данные
├── docs/                       # Тестовая документация
│   ├── diagrams/               # ERD и архитектурные диаграммы
│   └── test-management/        # Матрица тест-кейсов (Test Suite)
├── mcp/                        # Конфигурация Model Context Protocol
└── sql-tests/                  # SQL-скрипты проверки бизнес-правил
```

