# Deploy на VPS (Ubuntu)

1. Установить Docker + Compose plugin.
2. Открыть UFW порты 80/443.
3. Скопировать проект и `.env`.
4. Сгенерировать self-signed сертификат:
   ```bash
   mkdir -p deploy/certs
   openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
     -keyout deploy/certs/selfsigned.key \
     -out deploy/certs/selfsigned.crt -subj "/CN=<SERVER_IP>"
   ```
5. Запуск:
   ```bash
   docker compose up -d --build
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```
6. Обновление:
   ```bash
   git pull
   docker compose up -d --build
   ```

## Переход на Let's Encrypt после появления домена
- Выпустить сертификат через certbot (webroot или standalone).
- Поменять пути `ssl_certificate` и `ssl_certificate_key` в `nginx/default.conf`.
- Включить автообновление сертификатов (systemd timer certbot).
