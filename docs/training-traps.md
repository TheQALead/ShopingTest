# Training traps (TRAINING_TRAPS_MODE=on)

1. `auth/register`: поле `lastName` обязательно и должно быть пустой строкой `""`; иначе 400.
2. `cart/items`: поле `comment` обязательно и должно быть `""`; иначе 400.
3. `orders/{id}/pay`: заголовок `X-Client-Login` должен совпадать с email пользователя; иначе 403.
4. `products`: `page=0` -> 400.
5. `products`: `pageSize>100` -> 400.
6. `orders/{id}/pay`: при повторе без `Idempotency-Key` -> 409.
7. `products`: фильтр цены с запятой `19,99` ломается и отдаёт 400.
8. `orders`: пустая корзина -> 409.
9. `cards`: expYear в прошлом -> 400.
10. `cards`: brand может быть `UNKNOWN` даже для валидного BIN.
11. `auth/password-reset/confirm`: слишком короткий пароль возвращает общий 400 без детализации.
12. `orders/{id}/pay`: `declined` возвращает 402 и поле `reason` пустое.
13. `orders/{id}/pay/3ds-confirm`: неверный `mockCode` -> 400.
14. `products`: сортировка `name` чувствительна к регистру.
15. `cart/items/{id}`: qty=0 -> 400, qty<0 -> 422.
16. `admin/products`: hidden товар может попадать в поиск по ID.

Для каждого кейса студент должен фиксировать ОР/ФР и проверять контракты API.

17. `auth/login`: клиентское поле `type` влияет на роль. `Red power ranger` даёт `VIZOR` (намеренная уязвимость).
18. `admin/products` (POST): доступен ролям `ADMIN` и `VIZOR`, но `VIZOR` не имеет прав на PATCH категорий/товаров.
