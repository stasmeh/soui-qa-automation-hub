# ВАЖНО: Перед каждой командой (после двоеточия на следующей строке) 
# должен стоять знак TAB, а не пробелы!

# Переменные (упрощают настройку)
DC = docker compose
DB_CONTAINER = soui_qa_db
DB_USER = qa_admin
DB_NAME = soui_db

# Указываем, что это названия команд, а не имена файлов
.PHONY: help up down logs test-api test-sql

help: ## Показать список доступных команд
	@echo "Доступные команды:"
	@echo "  make up        - Собрать и запустить проект"
	@echo "  make down      - Остановить проект и очистить базу"
	@echo "  make logs      - Смотреть логи всех сервисов"
	@echo "  make test-api  - Запустить тесты Postman/Newman"
	@echo "  make test-sql  - Запустить SQL тесты"

up: ## Запустить контейнеры
	$(DC) up -d --build

down: ## Остановить контейнеры и удалить хранилища (чтобы БД инициализировалась заново)
	$(DC) down -v

logs: ## Посмотреть логи в реальном времени
	$(DC) logs -f

test-api: ## Запуск API тестов
	@echo "🚀 Запуск API тестов (Newman)..."
	npm install
	npm run test:api

test-sql: ## Запуск SQL тестов
	@echo "🐘 Запуск SQL тестов в базе данных..."
	@for file in tests/sql/*.sql; do \
		echo "Выполняю $$file..."; \
		docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) < "$$file" || true; \
	done