# Architecture — Foresight Engine

## Overview

Foresight Engine — платформа для предиктивной аналитики и мониторинга инфраструктуры в реальном времени. Система состоит из шести независимых сервисов, объединённых в единую сеть Docker.

## Схема системы

```
┌─────────────────────────────────────────────────────────────────┐
│                        foresight-net                            │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────────┐  │
│  │  Browser │───▶│ Frontend │───▶│  Backend (FastAPI)       │  │
│  └──────────┘    │  (Nginx) │    │  :8000                   │  │
│                  │  :80     │    │  /api/v1/                │  │
│                  └──────────┘    │  /health                 │  │
│                                  │  /metrics (Prometheus)   │  │
│                                  └──────────┬───────────────┘  │
│                                             │                   │
│               ┌─────────────────────────────┼────────────┐     │
│               │                             │            │     │
│               ▼                             ▼            ▼     │
│  ┌────────────────────┐  ┌──────────────────────┐  ┌────────┐ │
│  │ Agent Collector    │  │   PostgreSQL :5432   │  │ Redis  │ │
│  │ (Go)              │  │   - users            │  │ :6379  │ │
│  │ Metrics collector  │  │   - agents           │  │ db/0   │ │
│  │ via gopsutil       │  │   - metrics          │  │ db/1   │ │
│  │                    │  │   - predictions      │  │ db/2   │ │
│  │ Publishes to Redis │  └──────────────────────┘  │ db/3   │ │
│  └────────────────────┘                             └────────┘ │
│                                                          │      │
│               ┌──────────────────────────────────────────┘     │
│               │                                                  │
│               ▼                                                  │
│  ┌─────────────────────────────────────┐                        │
│  │ Celery Worker + Celery Beat         │                        │
│  │ (Python)                            │                        │
│  │  - aggregate_metrics (every minute) │                        │
│  │  - run_prediction (async tasks)     │                        │
│  │  - cleanup_old_predictions (daily)  │                        │
│  └─────────────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

## Сервисы

### Frontend (Nginx + React)
- **Порт**: 80 (443 для HTTPS)
- **Технологии**: React 18, TypeScript, Vite, Recharts, TanStack Query
- **Назначение**: SPA-интерфейс для просмотра метрик, агентов и прогнозов
- **Особенности**: статические файлы отдаются через Nginx; все запросы `/api/*` проксируются на backend; поддержка gzip-сжатия; security headers

### Backend (FastAPI)
- **Порт**: 8000
- **Технологии**: Python 3.12, FastAPI, SQLAlchemy async, Pydantic v2, Alembic
- **Назначение**: REST API, бизнес-логика, аутентификация, интеграция с Celery
- **Особенности**: 4 Uvicorn worker-процесса; async/await везде; Prometheus метрики на `/metrics`; JWT-аутентификация

### Agent Collector (Go)
- **Технологии**: Go 1.23, gopsutil, go-redis, pgx, zerolog
- **Назначение**: сбор системных метрик (CPU, RAM, Disk, Network) и публикация в Redis Pub/Sub
- **Особенности**: настраиваемый интервал сбора; graceful shutdown; нулевые зависимости на C

### Celery Worker
- **Технологии**: Python 3.12, Celery 5, Redis, scikit-learn, numpy
- **Назначение**: асинхронная обработка предсказаний, агрегация метрик по расписанию
- **Особенности**: concurrency 4; ack late для надёжности; beat-расписание вынесено в отдельный контейнер

### PostgreSQL
- **Версия**: 16 Alpine
- **Базы данных**: одна БД `foresight` с таблицами users, agents, metrics, predictions
- **Особенности**: healthcheck; инициализационный SQL; named volume для персистентности

### Redis
- **Версия**: 7 Alpine
- **Использование**:
  - DB 0 — Celery task queue и кеш backend
  - DB 1 — Pub/Sub канал agent-collector
  - DB 2 — Celery broker
  - DB 3 — Celery result backend
- **Особенности**: AOF persistence; парольная защита; healthcheck

## Поток данных

### Сбор метрик
```
OS → gopsutil → Agent Collector → Redis Pub/Sub (db/1) → Celery Worker → PostgreSQL
```

### API-запрос
```
Browser → Nginx → FastAPI → SQLAlchemy → PostgreSQL
                          → Redis (кеш/очередь)
                          → Celery (async task)
```

### Прогнозирование
```
POST /api/v1/predictions/ → FastAPI → PostgreSQL (создаёт запись)
                          → BackgroundTask → Celery → scikit-learn
                          → PostgreSQL (обновляет результат)
```

## Сетевая топология

Все сервисы работают в изолированной сети `foresight-net` (bridge driver). Наружу экспортируются только порты 80, 443 (frontend) и 8000 (backend для разработки). PostgreSQL (5432) и Redis (6379) открыты только на localhost для DBA-доступа.

## Хранение данных

| Volume | Сервис | Содержимое |
|---|---|---|
| `postgres_data` | postgres | Данные БД |
| `redis_data` | redis | AOF журнал |
| `backend_logs` | backend | JSON-логи |
| `agent_logs` | agent-collector | Логи агента |
| `celery_logs` | celery-worker | Логи воркера |
| `frontend_logs` | frontend | Nginx access/error |

## Мониторинг

- **Prometheus**: метрики FastAPI доступны на `http://backend:8000/metrics`
- **Structured logging**: все Python-сервисы пишут JSON-логи через structlog
- **Go logging**: zerolog с JSON-выводом
- **Health checks**: все сервисы имеют Docker healthcheck
