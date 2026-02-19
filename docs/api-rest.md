# REST API

Базовый путь: `/api/v1`.
Документация OpenAPI: `/api/schema/`, Swagger UI: `/api/docs/`.

Все endpoints (кроме register/login/refresh/verify/reset) требуют JWT Bearer токен.

## Основные коды
- 200/201: успех
- 400: ошибка валидации
- 401: нет/неверный токен
- 403: роль/ограничение доступа
- 409: конфликт (например пустая корзина/идемпотентность)

## Auth
- POST `/auth/register`
- POST `/auth/login`
- POST `/auth/refresh`
- POST `/auth/logout`
- GET `/auth/verify-email?token=...`
- POST `/auth/password-reset/request`
- POST `/auth/password-reset/confirm`

## Shop / Cart / Cards / Orders
Поддерживаются endpoints из ТЗ, включая сценарии оплаты `success|declined|requires_3ds`.

## Admin API
Только роль ADMIN:
- PATCH `/admin/products/{id}`
- POST `/admin/products`
- POST `/admin/categories`
- PATCH `/admin/categories/{id}`


## Учебная роль VIZOR
`POST /auth/login` в режиме тренировки учитывает поле `type` в body.
- `Green power ranger` -> `STUDENT`
- `Red power ranger` -> `VIZOR` (намеренная anti-pattern уязвимость для обучения).

Доступы:
- `VIZOR`: только `POST /api/v1/admin/products`
- `ADMIN`: полный admin API
