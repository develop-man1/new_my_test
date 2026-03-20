# Auth System

Backend-приложение с собственной системой аутентификации и авторизации на FastAPI + PostgreSQL.

## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy (async)** — ORM
- **PostgreSQL** — база данных
- **JWT (PyJWT)** — токены аутентификации
- **Argon2 (passlib)** — хэширование паролей
- **Pydantic v2** — валидация данных

---

## Запуск проекта

1. Клонировать репозиторий и установить зависимости:
```bash
pip install -r requirements.txt
```

2. Создать `.env` файл по образцу `.env.example`:
```dotenv
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
JWT_SECRET=ваш_секретный_ключ
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

3. Запустить приложение:
```bash
uvicorn app.main:app --reload
```

4. Заполнить БД тестовыми данными:
```bash
python -m app.seed
```

---

## Схема базы данных

### Таблица `users`
| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Первичный ключ |
| name | String | Имя |
| surname | String | Фамилия |
| patronymic | String | Отчество |
| email | String | Email (уникальный) |
| password | Text | Хэш пароля |
| role_id | Integer | FK → roles.id |
| is_active | Boolean | Статус аккаунта (soft delete) |
| created_at | DateTime | Дата регистрации |

### Таблица `roles`
| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Первичный ключ |
| name | String | Название роли (уникальное) |
| description | Text | Описание роли |

### Таблица `permissions`
| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Первичный ключ |
| resource | String | Ресурс (`products`, `orders`) |
| action | String | Действие (`read`, `create`, `update`, `delete`) |

> Уникальность по паре `(resource, action)`

### Таблица `role_permissions`
| Поле | Тип | Описание |
|------|-----|----------|
| role_id | Integer | FK → roles.id |
| permission_id | Integer | FK → permissions.id |

> Составной первичный ключ `(role_id, permission_id)`

---

## Система разграничения прав доступа (RBAC)

Используется модель **Role-Based Access Control (RBAC)**:

```
User → Role → RolePermission → Permission (resource + action)
```

### Логика проверки доступа

1. Пользователь логинится → получает JWT токен
2. При каждом запросе токен декодируется → извлекается `user_id`
3. По `user_id` загружается пользователь с его ролью и разрешениями
4. Проверяется: есть ли у роли разрешение на нужный `resource` + `action`
5. Если нет токена или токен невалидный → **401 Unauthorized**
6. Если токен валидный, но прав нет → **403 Forbidden**

### Тестовые роли

| Роль | products | orders |
|------|----------|--------|
| admin | read, create, update, delete | read, create, update, delete |
| moderator | read, create, update | read, create, update |
| user | read | read |

### Тестовые пользователи

| Email | Пароль | Роль |
|-------|--------|------|
| admin@test.com | admin1234 | admin |
| moderator@test.com | moder1234 | moderator |
| user@test.com | user1234 | user |

---

## API эндпоинты

### Auth `/auth`
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Вход (возвращает JWT) |
| POST | `/auth/logout` | Выход |

### Users `/users`
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| GET | `/users/me` | Получить свой профиль | Авторизованный |
| PATCH | `/users/me` | Обновить профиль | Авторизованный |
| DELETE | `/users/me` | Удалить аккаунт (soft) | Авторизованный |

### Admin `/admin`
| Метод | Путь | Описание | Доступ |
|-------|------|----------|--------|
| POST | `/admin/roles` | Создать роль | admin |
| POST | `/admin/permissions` | Создать разрешение | admin |

### Business `/business`
| Метод | Путь | Описание | Требуемое право |
|-------|------|----------|-----------------|
| GET | `/business/products` | Список продуктов | products:read |
| POST | `/business/products` | Создать продукт | products:create |
| GET | `/business/orders` | Список заказов | orders:read |
| DELETE | `/business/orders/{id}` | Удалить заказ | orders:delete |

---

## Soft Delete

При удалении аккаунта через `DELETE /users/me`:
- Запись в БД **не удаляется**
- Полю `is_active` устанавливается значение `False`
- Пользователь больше не может войти в систему (401)
- Данные сохраняются в базе

---

## Структура проекта

```
app/
├── core/
│   ├── config.py        # Настройки приложения
│   ├── database.py      # Подключение к БД
│   └── security.py      # JWT, хэширование паролей
├── models/
│   ├── user.py
│   ├── role.py
│   ├── permission.py
│   └── role_permission.py
├── schemas/
│   ├── user.py
│   ├── role.py
│   └── permission.py
├── crud/
│   ├── user_crud.py
│   ├── role_crud.py
│   └── permission_crud.py
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   ├── role_service.py
│   └── permission_service.py
├── dependencies/
│   └── auth.py          # get_active_user, get_admin_user, require_permission
├── routes/
│   ├── auth.py
│   ├── users.py
│   ├── admin.py
│   └── mock_business.py
├── seed.py              # Тестовые данные
└── main.py
```