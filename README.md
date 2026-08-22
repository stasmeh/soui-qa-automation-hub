[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 🎓 СОУИ — QA Engineering Hub (Sandbox with Gemini & MCP)

Тестовый стенд и комплекс обеспечения качества для **Системы Обработки Учебной Информации (СОУИ)**. Проект служит учебной песочницей для практической демонстрации навыков тестирования REST API, реляционных баз данных (PostgreSQL), анализа сетевого трафика (Charles Proxy), а также интеграции ИИ-агентов на базе моделей Gemini через протокол Model Context Protocol (MCP).

---

## 🛠️ Технологический стек проекта

* **Backend / API**: Python 3.11, FastAPI, SQLAlchemy, Pydantic, Uvicorn
* **Database**: PostgreSQL 16
* **QA & Test Design**: Test Cases Suite, ERD-диаграммы, MindMap (XMind)
* **API Testing Tools**: Postman (коллекция в репозитории), Newman CLI, Swagger / ReDoc
* **Traffic Inspection**: Charles Proxy
* **AI Integration**: Model Context Protocol (MCP), Gemini Prompts (в `.agent/prompts/`)
* **DevOps**: Docker, Docker Compose

---

## 📌 Структура проекта и артефакты

```text
soui-qa-automation-hub/
├── .agent/prompts/             # Промпты для AI QA-агента (Gemini)
│   ├── qa_analyst.prompt.md    # Инструкция по генерации тест-кейсов по ISO/IEC/IEEE 29119
│   ├── sql_validator.prompt.md # Скрипт-промпт для аудита ограничений схемы БД
│   └── bug_reporter.prompt.md  # Шаблон для локализации и оформления баг-репортов
├── app/                        # REST API бэкенд на FastAPI
│   ├── database.py             # Подключение к PostgreSQL через SQLAlchemy
│   ├── main.py                 # Эндпоинты для 8 сущностей системы
│   ├── models.py               # ORM-модели таблиц
│   └── requirements.txt        # Список зависимостей Python
├── docker/                     # Контейнеризация
│   ├── docker-compose.yml      # Оркестрация контейнеров API и СУБД
│   └── init-db/                # DDL схемы и начальные данные PostgreSQL
│       ├── 01_schema.sql       # Определение таблиц и CHECK-констреинтов
│       └── 02_seed_data.sql    # Тестовый датасет
├── docs/                       # Тестовая документация
│   ├── diagrams/               # Архитектурная MindMap и ER-диаграмма
│   └── test-management/        # Набор тест-кейсов (Test Cases Suite)
├── mcp/                        # Конфигурация Model Context Protocol для ИИ-агентов
│   └── cline_mcp_settings.json # Подключение MCP Postgres сервера
├── sql-tests/                  # SQL-скрипты проверки бизнес-правил СУБД
└── tests/                      # Инструменты тестирования API
    └── soui_postman_collection.json # Импортируемая коллекция запросов Postman с тестами
```

---

## 🧩 Сущности предметной области (Data Model Overview)

Система построена вокруг 8 взаимосвязанных реляционных сущностей:

| Сущность | Таблица БД | Назначение | Ключевые ограничения и правила целостности |
| :--- | :--- | :--- | :--- |
| **Специальность** | `specialty` | Направления подготовки | `name` и `code_spec` — только кириллица (`CHECK ~ '^[А-Яа-яЁё\s]+$'`), уникальный код |
| **Группа** | `student_group` | Академические группы | Ссылка на `specialty` (`ON DELETE RESTRICT`), уникальный код группы |
| **Студент** | `student` | Учащиеся вуза | ФИО на кириллице, уникальный номер студбилета, форма обучения: `'платное'` / `'бюджетное'` |
| **Преподаватель** | `teacher` | Профессорско-преподавательский состав | ФИО, кафедра и должность — только кириллица |
| **Дисциплина** | `subject` | Учебные предметы | Положительное кол-во часов и семестров (`hours_count > 0`, `semesters_count > 0`) |
| **Задание** | `assignment` | Варианты контрольных заданий | Привязка к дисциплине (`ON DELETE RESTRICT`), номер варианта и текст |
| **Контрольная точка** | `control_point` | Рубежные срезы знаний | Название контрольной точки (кириллица, цифры, пробелы) |
| **Журнал успеваемости** | `journal` | Фиксация оценок | Связи со всеми ключевыми сущностями, балл строго в диапазоне `0..60` (`CHECK grade BETWEEN 0 AND 60`) |

---

## ⚙️ Инструкция по запуску стенда

### Предварительные требования (Prerequisites)
* Установленный **Docker Engine** (20.10+) и **Docker Compose** (v2+)
* Свободные локальные порты: `8000` (FastAPI) и `5432` (PostgreSQL)

### Запуск сервисов
Для развертывания веб-сервиса и базы данных PostgreSQL с автоматическим накатыванием схемы и тестового наполнения выполните:

```bash
docker-compose -f docker/docker-compose.yml up --build -d
```

### Интерфейсы запущенной системы
* **Интерактивная документация Swagger API**: `http://localhost:8000/docs`
* **Альтернативная документация ReDoc**: `http://localhost:8000/redoc`
* **База данных PostgreSQL**: доступна по порту `5432`
  * *Host*: `localhost` / *Port*: `5432`
  * *Database*: `soui_db`
  * *User*: `qa_admin`
  * *Password*: `qa_secure_password` *(только для тестового окружения)*

---

## 🧪 Запуск тестов из терминала (CLI)

### 1. Выполнение SQL-проверок целостности данных
Скрипты валидации ограничений целостности и аналитических отчетов можно запустить напрямую в контейнере БД:

```bash
# Проверка CHECK-ограничений и ссылочной целостности
docker exec -i soui_qa_db psql -U qa_admin -d soui_db < sql-tests/01_integrity_and_constraints.sql

# Формирование сводного отчета успеваемости
docker exec -i soui_qa_db psql -U qa_admin -d soui_db < sql-tests/02_business_logic_reports.sql
```

### 2. Запуск API-тестов Postman через Newman CLI
Коллекцию тестов можно запустить без графического интерфейса с помощью Newman:

```bash
# Быстрый прогон всех эндпоинтов с выводом результатов в консоль
npx newman run tests/soui_postman_collection.json --env-var "baseUrl=http://localhost:8000"
```

---

## 📑 Описание реализованных QA-активностей

### 1. Тестирование баз данных (Database Testing)
В папке `sql-tests/` подготовлены SQL-скрипты для валидации ограничений целостности данных:
* `01_integrity_and_constraints.sql`: Проверка `CHECK`-констреинтов (валидация ФИО на кириллицу, диапазон оценок `0-60`) и ограничений ссылочной целостности (`ON DELETE RESTRICT` на связях).
* `02_business_logic_reports.sql`: Аналитический SQL-запрос для формирования сводной успеваемости и выявления задолженностей студентов.

### 2. Тест-дизайн и тест-кейсы
В файле [`docs/test-management/Test_Cases_Suite.md`](docs/test-management/Test_Cases_Suite.md) описаны тест-кейсы для всех разделов системы. Применены следующие техники тест-дизайна:
* **Анализ граничных значений (BVA)** для проверки лимита оценок в журнале (`0..60` баллов: `-1, 0, 1, 59, 60, 61`).
* **Эквивалентное разделение (EP)** для валидации полей ФИО (кириллица, латиница, спецсимволы, пустые значения).
* **Таблица переходов состояний (State Transition)** для жизненного цикла записи успеваемости в журнале.

### 3. Тестирование API (Postman & Newman)
В папке `tests/` находится файл `soui_postman_collection.json`. Коллекция включает:
* Сгруппированные по папкам REST API запросы к FastAPI.
* Встроенные JS-тесты (проверки статус-кодов, соответствие форматов ответов JSON Schema).
* Переменные окружения для гибкого переключения хоста.

### 4. Интеграция с ИИ-агентами (Gemini & MCP)
Репозиторий адаптирован для совместной работы с ИИ-агентами (Cline, Cursor) через протокол **Model Context Protocol (MCP)**:
* Файл `mcp/cline_mcp_settings.json` содержит конфигурацию подключения агента к PostgreSQL.
* Инструкции в `.agent/prompts/` (например, `qa_analyst.prompt.md`) позволяют ИИ читать схему базы данных напрямую, проводить сверку ожидаемого и фактического состояний данных в СУБД, а также автоматизировать написание баг-репортов.

#### 🤖 Пошаговый сценарий запуска аудита через ИИ-агента:
1. Скопируйте блок из `mcp/cline_mcp_settings.json` в глобальные настройки MCP вашего ассистента.
2. Убедитесь, что контейнер `soui_qa_db` запущен на порту `5432`.
3. Задайте агенту задачу, сославшись на промпт:
   > *"Используя инструкцию `.agent/prompts/sql_validator.prompt.md`, выполни аудит таблиц `student` и `journal` и сформируй список потенциальных дефектов схемы."*

---

## 📊 Диаграммы и архитектура

| ER-диаграмма базы данных | MindMap архитектуры |
| :---: | :---: |
| <img src="docs/diagrams/erd_schema_soui.jpg" width="450" alt="ER-диаграмма" /> | <img src="docs/diagrams/mindmap_soui.jpg" width="450" alt="MindMap" /> |

---

## 👤 Автор и контакты

* **QA Engineer**: Станислав
* **GitHub**: [@stasmeh](https://github.com/stasmeh)
* **Репозиторий**: [soui-qa-automation-hub](https://github.com/stasmeh/soui-qa-automation-hub)
