# Памятка по установке и запуску ShoeStore

Учебный проект десктопного приложения «Магазин обуви» (ShoeShop), упакованный в исполняемый пакет Windows (PyInstaller onedir) с внешней базой данных PostgreSQL в Docker Compose.

---

## 1. Системные требования
- Операционная система: **Windows 10 / Windows 11 (64-бит)**;
- СУБД: запущенный **Docker Desktop** (контейнер на порту 5433) либо локальная служба **PostgreSQL** (порт 5432);
- Для запуска собранного EXE установка локального Python **не требуется** (интерпретатор и библиотеки упакованы в приложение).

---

## 2. Развёртывание базы данных PostgreSQL в Docker Compose
1. Создайте файл локальных переменных окружения `.env` на основе шаблона `.env.example`:
   ```powershell
   copy .env.example .env
   ```
2. Параметры базы данных:
   ```dotenv
   POSTGRES_DB=shoe_shop
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=p@ssw0rd
   POSTGRES_HOST_PORT=5433
   ```
3. Запустите контейнеры СУБД:
   ```powershell
   docker compose up -d
   ```
4. При первом запуске на пустом томе импортируйте дамп базы данных:
   ```powershell
   docker compose cp database/shoe_store.sql db:/tmp/shoe_store.sql
   docker compose exec db psql -v ON_ERROR_STOP=1 -U postgres -d shoe_shop -f /tmp/shoe_store.sql
   ```
5. Проверьте состояние СУБД диагностическим сервисом:
   ```powershell
   docker compose run --rm db-check
   ```
   Ожидаемый ответ: `OK: база=shoe_shop; таблиц=5`.

---

## 3. Настройка параметров подключения (config.ini)
Конфигурационный файл приложения находится в каталоге `dist\ShoeStore\config.ini`:
```ini
[database]
host = 127.0.0.1
port = 5433
name = shoe_shop
user = postgres
password = p@ssw0rd
```
- Для Docker Compose укажите `port = 5433`;
- Для локальной СУБД PostgreSQL укажите `port = 5432`.

---

## 4. Запуск исполняемого файла
Запуск из каталога проекта:
```powershell
.\dist\ShoeStore\ShoeStore.exe
```
Либо двойным кликом по файлу `ShoeStore.exe` в папке `dist\ShoeStore`. Приложение откроет окно каталога обуви, загрузит товары и фотографии из каталога `import`.

---

## 5. Управление сервисами Docker
- Остановка контейнеров: `docker compose stop`
- Запуск контейнеров: `docker compose start`
- Удаление контейнеров (том сохраняется): `docker compose down`
