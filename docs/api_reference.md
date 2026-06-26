# API Reference — Foresight Engine

Base URL: `http://localhost:8000/api/v1`
Interactive docs: `http://localhost:8000/docs` (Swagger UI)

## Authentication

Все эндпоинты (кроме `/health`, `/auth/register`, `/auth/token`) требуют JWT-токен в заголовке:

```
Authorization: Bearer <access_token>
```

---

## Health

### GET /health
Проверка работоспособности сервиса.

**Response 200**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

---

## Auth — `/api/v1/auth`

### POST /auth/register
Регистрация нового пользователя.

**Request Body**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response 201**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

### POST /auth/token
Получение JWT токена (OAuth2 Password Flow).

**Request** (form-data)
```
username=john_doe
password=secure_password
```

**Response 200**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### GET /auth/me
Получение текущего пользователя.

**Response 200**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

## Agents — `/api/v1/agents`

### GET /agents/
Список всех агентов.

**Query Parameters**
| Параметр | Тип | По умолч. | Описание |
|---|---|---|---|
| `limit` | int | 50 | Количество записей |
| `offset` | int | 0 | Смещение |

**Response 200**
```json
[
  {
    "id": 1,
    "name": "prod-server-01",
    "description": "Production server in EU-West",
    "status": "active",
    "config": {"region": "eu-west-1"},
    "last_seen": "2024-10-01T12:00:00Z",
    "created_at": "2024-09-01T00:00:00Z"
  }
]
```

---

### POST /agents/
Создание нового агента.

**Request Body**
```json
{
  "name": "prod-server-01",
  "description": "Production server in EU-West",
  "config": {
    "region": "eu-west-1",
    "tags": ["prod", "web"]
  }
}
```

**Response 201** — объект агента

---

### GET /agents/{agent_id}
Получение агента по ID.

**Response 200** — объект агента
**Response 404**
```json
{"detail": "Agent not found"}
```

---

### PATCH /agents/{agent_id}
Обновление агента.

**Request Body** (все поля опциональны)
```json
{
  "name": "new-name",
  "status": "inactive",
  "description": "Updated description",
  "config": {}
}
```

**Response 200** — обновлённый объект агента

---

### DELETE /agents/{agent_id}
Удаление агента.

**Response 204** — No Content

---

## Metrics — `/api/v1/metrics`

### GET /metrics/
Список метрик с фильтрацией.

**Query Parameters**
| Параметр | Тип | Описание |
|---|---|---|
| `agent_id` | int | Фильтр по агенту |
| `metric_type` | string | Тип метрики (cpu_percent, memory_percent, ...) |
| `from_dt` | datetime | Начало диапазона (ISO 8601) |
| `to_dt` | datetime | Конец диапазона (ISO 8601) |
| `limit` | int | Макс. 1000, по умолч. 100 |
| `offset` | int | Смещение |

**Response 200**
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "metric_type": "cpu_percent",
    "value": 42.5,
    "metadata": {"host": "prod-server-01"},
    "timestamp": "2024-10-01T12:00:00Z"
  }
]
```

---

### POST /metrics/
Запись новой метрики.

**Request Body**
```json
{
  "agent_id": 1,
  "metric_type": "cpu_percent",
  "value": 42.5,
  "metadata": {"host": "local"},
  "timestamp": "2024-10-01T12:00:00Z"
}
```

**Response 201** — объект метрики

---

### GET /metrics/summary
Агрегированная сводка метрик.

**Response 200**
```json
{
  "total": 15420,
  "agents": 3,
  "metric_types": ["cpu_percent", "memory_percent", "disk_percent", "net_bytes_sent"]
}
```

---

### GET /metrics/{metric_id}
Метрика по ID.

**Response 200** — объект метрики

---

## Predictions — `/api/v1/predictions`

### GET /predictions/
Список прогнозов.

**Query Parameters**
| Параметр | Тип | По умолч. |
|---|---|---|
| `limit` | int | 50 |
| `offset` | int | 0 |

**Response 200**
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "model_type": "linear_regression",
    "horizon_hours": 24,
    "status": "completed",
    "result": {
      "forecast": [41.2, 39.8, 45.1],
      "confidence": 0.95,
      "model": "linear_regression"
    },
    "created_at": "2024-10-01T12:00:00Z",
    "completed_at": "2024-10-01T12:00:05Z"
  }
]
```

---

### POST /predictions/
Создание нового прогноза (асинхронно).

**Request Body**
```json
{
  "agent_id": 1,
  "model_type": "linear_regression",
  "horizon_hours": 24,
  "parameters": {
    "features": ["cpu_percent", "memory_percent"],
    "lookback_hours": 72
  }
}
```

**Response 202** — объект прогноза со статусом `pending`

---

### GET /predictions/{prediction_id}
Прогноз по ID.

**Response 200** — объект прогноза

---

## Статусы агентов

| Статус | Описание |
|---|---|
| `active` | Агент активен и отправляет данные |
| `inactive` | Агент отключён |
| `error` | Агент сообщает об ошибке |

## Статусы прогнозов

| Статус | Описание |
|---|---|
| `pending` | Задача создана, ожидает очереди |
| `running` | Модель выполняется |
| `completed` | Прогноз готов |
| `failed` | Ошибка выполнения |

## Типы метрик (Agent Collector)

| Тип | Единица | Описание |
|---|---|---|
| `cpu_percent` | % | Загрузка CPU |
| `memory_percent` | % | Использование RAM |
| `memory_bytes_used` | bytes | RAM в байтах |
| `disk_percent` | % | Использование диска на `/` |
| `net_bytes_sent` | bytes | Исходящий сетевой трафик |
| `net_bytes_recv` | bytes | Входящий сетевой трафик |

## Коды ошибок

| Код | Описание |
|---|---|
| 400 | Bad Request — ошибка валидации |
| 401 | Unauthorized — невалидный или отсутствующий токен |
| 404 | Not Found — ресурс не найден |
| 422 | Unprocessable Entity — ошибка схемы запроса |
| 500 | Internal Server Error |
