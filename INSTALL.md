# Инструкция по установке и запуску ShoeStore

Учебный проект десктопного приложения «Магазин обуви» (ShoeShop), упакованный в исполняемый пакет Windows (PyInstaller onedir) с внешней базой данных PostgreSQL в Docker Compose.

---

## 1. Системные требования
- Операционная система: **Windows 10 / Windows 11 (64-бит)**;
- Установленный и запущенный **Docker Desktop** (режим Linux containers, подсистема WSL 2);
- Установленный плагин **Docker Compose v2** (`docker compose version`);
- Установка локального Python на целевом компьютере **не требуется** (интерпретатор и библиотеки упакованы в приложение).

---

## 2. Развёртывание базы данных PostgreSQL в Docker
База данных не встроена внутрь `ShoeStore.exe`, а развёртывается как изолированный сервис:

1. Перейдите в каталог `deployment/`:
   ```powershell
   cd deployment
   ```
2. Создайте файл локальных переменных окружения `.env` на основе шаблона `.env.example`:
   ```powershell
   copy .env.example .env
   ```
3. Откройте `.env` в текстовом редакторе и задайте параметры подключения (по умолчанию: база `shoe_store`, пользователь `shoe_user`, порт хоста `5433`):
   ```dotenv
   POSTGRES_DB=shoe_store
   POSTGRES_USER=shoe_user
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_HOST_PORT=5433
   ```
4. Запустите СУБД PostgreSQL и проверку готовности `healthcheck`:
   ```powershell
   docker compose up -d
   ```
5. При первом запуске (если база пустая) импортируйте структуру таблиц и данные:
   ```powershell
   docker compose cp database/shoe_store.sql db:/tmp/shoe_store.sql
   docker compose exec db psql -v ON_ERROR_STOP=1 -U shoe_user -d shoe_store -f /tmp/shoe_store.sql
   ```
6. Убедитесь, что контейнер находится в состоянии `healthy`:
   ```powershell
   docker compose ps
   ```

---

## 3. Настройка конфигурации приложения
1. В каталоге с исполняемым файлом `application/ShoeStore/` (рядом с `ShoeStore.exe`) создайте конфигурационный файл `config.ini` на основе `config.ini.example`:
   ```powershell
   copy config.ini.example application\ShoeStore\config.ini
   ```
2. Отредактируйте `application\ShoeStore\config.ini`, указав порт хоста `5433` и пароль из `.env`:
   ```ini
   [database]
   host = localhost
   port = 5433
   name = shoe_store
   user = shoe_user
   password = your_secure_password
   ```

---

## 4. Запуск приложения
Запустите исполняемый файл:
```powershell
.\application\ShoeStore\ShoeStore.exe
```
При запуске откроется главное окно каталога обуви. Программа автоматически подключится к PostgreSQL по адресу `localhost:5433` и загрузит товары, категории, скидки и фотографии.

---

## 5. Остановка и управление инфраструктурой
- Остановка контейнеров с сохранением данных:
  ```powershell
  cd deployment
  docker compose stop
  ```
- Возобновление работы:
  ```powershell
  docker compose start
  ```
- **ВНИМАНИЕ:** Команда `docker compose down -v` удаляет именованный том и стирает все данные базы! При штатной остановке используйте `docker compose down` (без ключа `-v`) или `docker compose stop`.

---

## 6. Возможные проблемы и диагностика
1. **Ошибка «Could not connect to PostgreSQL server»:**  
   Убедитесь, что Docker Desktop запущен, выполните `docker compose ps` в каталоге `deployment` и проверьте, что порт `5433` в `config.ini` совпадает с `POSTGRES_HOST_PORT` в `.env`.
2. **Не отображаются фотографии товаров:**  
   Убедитесь, что папка `import/` скопирована рядом с `ShoeStore.exe` или находится в `_internal/import`.
