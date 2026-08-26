FROM python:3.11-slim

# Отключаем буферизацию вывода и генерацию .pyc файлов
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Устанавливаем системные зависимости (если нужны для сборки драйверов БД)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Сначала копируем только зависимости для кэширования слоев
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY app/ ./app

# Открываем порт сервиса
EXPOSE 8000

# Базовая команда запуска (БЕЗ флага --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]