# User Guide — Foresight Engine

## Требования

- Docker >= 24.0
- Docker Compose >= 2.20
- GNU Make
- Git
- 4 GB RAM минимум
- 10 GB свободного места на диске

## Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/your-org/foresight-engine.git
cd foresight-engine
```

### 2. Настроить переменные окружения
```bash
cp .env.example .env
```
Откройте `.env` и замените все значения по умолчанию:

| Переменная | Описание | Пример |
|---|---|---|
| `POSTGRES_DB` | Имя базы данных | `foresight` |
| `POSTGRES_USER` | Пользователь PostgreSQL | `foresight_user` |
| `POSTGRES_PASSWORD` | **Обязательно изменить** | `MyStr0ngP@ss!` |
| `REDIS_PASSWORD` | **Обязательно изменить** | `RedisP@ss2024` |
| `SECRET_KEY` | JWT-секрет, мин. 32 символа | `$(openssl rand -hex 32)` |
| `DEBUG` | Режим отладки | `false` |
| `ALLOWED_ORIGINS` | CORS-разрешённые origins | `https://yourdomain.com` |
| `LOG_LEVEL` | Уровень логирования | `info` |
| `COLLECTION_INTERVAL` | Интервал сбора метрик (сек) | `60` |
| `VITE_API_URL` | URL backend для frontend | `https://yourdomain.com` |

### 3. Запустить систему
```bash
make run-dev
```
Или напрямую:
```bash
docker compose up -d
```

### 4. Проверить работу
```bash
make ps
curl http://localhost:8000/health
```

**Доступные адреса:**
- Веб-интерфейс: http://localhost
- API: http://localhost:8000/api/v1
- Swagger UI: http://localhost:8000/docs
- Prometheus метрики: http://localhost:8000/metrics

---

## Разработка

### Сборка образов
```bash
make build-core
```

### Запуск отдельного сервиса
```bash
docker compose up -d backend
docker compose up -d agent-collector
```

### Просмотр логов
```bash
make logs                  # все сервисы
make logs-backend          # только backend
make logs-agent            # только agent-collector
make logs-celery           # только celery-worker
```

### Shell в контейнере
```bash
make shell-backend         # bash в backend
make shell-db              # psql
make shell-redis           # redis-cli
```

### Миграции базы данных
```bash
make migrate                         # применить все миграции
make migrate-create name="add_tags"  # создать новую миграцию
```

---

## Тестирование

### Запуск всех тестов
```bash
make test
```

### Запуск тестов по сервису
```bash
make test-backend     # pytest для FastAPI
make test-go          # go test для agent-collector
make test-celery      # pytest для celery-worker
```

### Линтинг кода
```bash
make lint
```

---

## Работа с API

### Регистрация пользователя
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"password123"}'
```

### Получение токена
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/token \
  -F "username=admin" \
  -F "password=password123" | jq -r .access_token)
```

### Создание агента
```bash
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-server","description":"Main production server"}'
```

### Отправка метрики вручную
```bash
curl -X POST http://localhost:8000/api/v1/metrics/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":1,"metric_type":"cpu_percent","value":42.5}'
```

### Запуск прогноза
```bash
curl -X POST http://localhost:8000/api/v1/predictions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":1,"model_type":"linear_regression","horizon_hours":24}'
```

---

## Деплой в продакшн

### Через Makefile
```bash
make deploy
```

### Ручной деплой
```bash
docker compose pull
docker compose up -d --remove-orphans
docker image prune -f
```

### CI/CD через GitHub Actions
1. Добавьте секреты в настройках репозитория:
   - `DEPLOY_HOST` — IP или hostname сервера
   - `DEPLOY_USER` — SSH пользователь
   - `DEPLOY_SSH_KEY` — приватный SSH ключ
2. Push в ветку `main` автоматически запустит деплой после прохождения всех тестов.

---

## Устранение проблем

### Сервис не запускается
```bash
docker compose ps
docker compose logs <service_name>
```

### PostgreSQL не принимает подключения
```bash
docker compose exec postgres pg_isready -U $POSTGRES_USER
```

### Redis недоступен
```bash
docker compose exec redis redis-cli -a $REDIS_PASSWORD ping
```

### Порт занят
```bash
# Проверить, кто занимает порт 80
sudo lsof -i :80
# Изменить порт в docker-compose.yml или остановить конфликтующий сервис
```

### Очистить всё и начать заново
```bash
make clean
make run-dev
```

---

## Мониторинг

### Prometheus
Метрики FastAPI доступны по адресу `http://localhost:8000/metrics`. Подключите Prometheus с конфигом:

```yaml
scrape_configs:
  - job_name: foresight-backend
    static_configs:
      - targets: ['backend:8000']
```

### Просмотр метрик Redis
```bash
make shell-redis
> INFO stats
> DBSIZE
```

### Просмотр очереди Celery
```bash
docker compose exec celery-worker celery -A app.celery_app inspect active
docker compose exec celery-worker celery -A app.celery_app inspect reserved
```

---

## Структура проекта

```
foresight-engine/
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
├── Makefile
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/v1/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── models/
│   └── tests/
├── agent-collector/
│   ├── Dockerfile
│   ├── go.mod
│   ├── cmd/collector/
│   └── internal/
│       ├── collector/
│       ├── publisher/
│       └── config/
├── celery-worker/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── celery_app.py
│   │   └── tasks/
│   └── tests/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── api/
│       ├── components/
│       └── pages/
├── nginx/
│   └── nginx.conf
├── scripts/
│   └── init.sql
└── docs/
    ├── architecture.md
    ├── api_reference.md
    └── user_guide.md
```
