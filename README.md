# Training Shop

Учебный публичный сайт интернет-магазина-симулятора для практики QA (UI/REST/SOAP).

## Стек
- Python 3.12, Django, DRF
- PostgreSQL
- JWT access/refresh
- Swagger/OpenAPI (drf-spectacular)
- SOAP endpoint + WSDL
- Docker Compose (web + db + nginx)
- Логирование REST/SOAP запросов

## Быстрый старт
```bash
cp .env.example .env
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Доступ:
- UI/API: `https://<IP>`
- Admin: `https://<IP>/admin/`
- Swagger: `https://<IP>/api/docs/`
- SOAP WSDL: `https://<IP>/soap/v1/TrainingShopService?wsdl`

## Demo users
- student@example.com / Password123!
- admin@example.com / Password123!
- vizor@example.com / Password123!

## Invite-code регистрация
Регистрация доступна только с валидным invite-кодом.
Invite-коды создаются и управляются через Django Admin.

## Email verification + password reset
Подтверждение email и сброс пароля обязательны.
Письма только на русском.

### Настройка SMTP Яндекс
В `.env`:
- `EMAIL_HOST=smtp.yandex.ru`
- `EMAIL_PORT=465`
- `EMAIL_USE_SSL=true`
- `EMAIL_HOST_USER=<yandex_login>`
- `EMAIL_HOST_PASSWORD=<app_password_or_password>`
- `DEFAULT_FROM_EMAIL="Training Shop <trainingshop.qa@yandex.ru>"`

Рекомендуется:
1. Создать отдельный ящик для проекта.
2. Включить пароль приложения (если требуется политикой Яндекса).
3. Проверить отправку:
```bash
docker compose exec web python manage.py shell -c "from django.core.mail import send_mail; send_mail('Тест','Проверка SMTP','trainingshop.qa@yandex.ru',['your@mail.ru'])"
```

## TRAINING_TRAPS_MODE
По умолчанию `on`.
- `on`: включены учебные ловушки API.
- `off`: ловушки выключены.

## Документация
- `docs/api-rest.md`
- `docs/api-soap.md`
- `docs/training-scenarios.md`
- `docs/training-bugs.md`
- `docs/training-traps.md`
- `deploy/README.md`
- `tools/postman_collection.json`


## Учебная security-пасхалка в логине
В `TRAINING_TRAPS_MODE=on` endpoint `/api/v1/auth/login` читает поле `type` из тела запроса.
- Для обычного входа студента ожидается `Type: Green power ranger`.
- Если подменить на `Type: Red power ranger`, backend ошибочно выдаёт роль `VIZOR` (намеренная уязвимость для тренировки).

`VIZOR` может добавлять товар через `POST /api/v1/admin/products`, но не может изменять категории и редактировать товар.
