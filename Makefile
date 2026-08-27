# ВАЖНО: Перед каждой командой (где отступ) должен стоять знак TAB, а не пробелы!

# Переменные (для удобства, если названия поменяются, их легко изменить в одном месте)
DC = docker compose
DB_CONTAINER = soui_qa_db
DB_USER = qa_admin
DB_NAME = soui_db

# Эта строчка говорит Make, что это не файлы, а команды
.PHONY: help up down logs test-api test-sql

help: ## Показать список доступных команд
	@echo "Доступные команды:"
	@echo "  make up        - Собрать и запустить проект"
	@echo "  make down      - Остановить проект"
	@echo "  make logs      - Смотреть логи всех сервисов"
	@echo "  make test-api  - Запустить тесты Postman/Newman"
	@echo "  make test-sql  - Запустить SQL тесты"

up: ## Запустить контейнеры
	$(DC) up -d --build

down: ## Остановить контейнеры
	$(DC) down

logs: ## Посмотреть логи в реальном времени
	$(DC) logs -f

test-api: ## Запуск API тестов
	@echo "🚀 Запуск API тестов (Newman)..."
	# Если ваш package.json лежит в папке tests/postman, используйте эту команду:
	cd tests/postman && npm install && npm test
	# Если package.json остался в корне проекта, поменяйте на: npm install && npm test

test-sql: ## Запуск SQL тестов
	@echo "🐘 Запуск SQL тестов в базе данных..."
	# Пример: прогоняем SQL-скрипты через контейнер базы данных.
	# Если файлы лежат в tests/sql/, скрипт найдет их и выполнит:
	for file in tests/sql/*.sql; do \
		echo "Выполняю $$file..."; \
		docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) < "$$file"; \
	done