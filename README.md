# 🎓 СОУИ — QA Automation & Test Engineering Hub

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Model Context Protocol](https://img.shields.io/badge/MCP-PostgreSQL-8A2BE2?style=flat-square)](https://modelcontextprotocol.io)

Тестовый стенд и комплекс автоматизации тестирования для **Системы обработки учебной информации (СОУИ)**. Проект демонстрирует полный цикл обеспечения качества: валидацию схемы СУБД, REST API тестирование (CRUD, фильтрация, отчеты), проверку сетевого трафика и интеграцию AI-агентов через протокол MCP.

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
##

🎯 Матрица покрытия тестированиемУровеньПроверяемый функционалИнструментыЦелостность БДОграничения CHECK (оценки 0–60, часы > 0), UNIQUE, ON DELETE RESTRICTPostgreSQL, SQL DDLREST APIЖизненный цикл 8 сущностей (CRUD), HTTP-статусы 200, 201, 400, 404, 409FastAPI, Swagger UIБизнес-логикаКонтекстный режим преподавателя, сводные ведомости с агрегацией (AVG, COUNT)SQLAlchemy, SQL Group ByСетевой уровеньОбход клиентской валидации через Breakpoints, подмена ответов (Map Local)Charles Proxy, FiddlerAI QA AutomationАвтономный аудит схемы БД, выполнение тестов и генерация баг-репортовGemini, Roo Code / Cline, MCP
