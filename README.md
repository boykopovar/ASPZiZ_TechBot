# ASPZiZ_TechBot

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![aiogram](https://img.shields.io/badge/aiogram-3.x-blue)
![aiosqlite](https://img.shields.io/badge/aiosqlite-latest-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

Telegram-бот технической поддержки. Принимает заявки от пользователей в личных сообщениях, публикует их в авторизованных групповых чатах поддержки, управляет жизненным циклом тикетов и правами доступа.

---

## Стек

- Python 3.8+, полные аннотации типов
- [aiogram](https://docs.aiogram.dev/) 3.x - асинхронный Telegram Bot API
- [aiosqlite](https://aiosqlite.omnilib.dev/) - асинхронный SQLite
- [python-dotenv](https://pypi.org/project/python-dotenv/) - конфигурация через `.env`
- Docker / Docker Compose

---

## Архитектура

| Слой | Модуль | Ответственность | Зависит от |
|---|---|---|---|
| Транспорт | `handlers/` | Приём событий Telegram (команды, callback, сообщения), валидация прав, вызов сервисов | `services/`, `types/`, `utils/`, `constants` |
| Сервисы | `services/` | Бизнес-логика: создание тикетов, смена статусов, публикация в чаты, управление пользователями | `repositories/`, `constants` |
| Репозиторий | `repositories/` | Единственная точка работы с БД. Все SQL-запросы, инициализация схемы | `env_tools` (путь к БД) |
| Типы | `types/` | Перечисления (`Role`, `TicketStatus`, `MediaType`), CallbackData-классы | ничего |
| Утилиты | `utils/` | Форматирование текста, генерация клавиатур, отправка медиа | `types/`, `constants` |
| Инфраструктура | `env_tools`, `logger`, `constants` | Конфигурация из `.env`, настройка логгера, строковые константы | ничего |

---

## База данных

SQLite, 6 таблиц:

| Таблица | Назначение |
|---|---|
| `users` | Пользователи: `telegram_id`, `username`, `role` |
| `tickets` | Заявки: `user_id`, `text`, `status`, `created_at` |
| `ticket_media` | Медиафайлы заявки: `ticket_id`, `type`, `file_id` |
| `support_chats` | Чаты поддержки: `chat_id`, `title`, `is_active`, `approved_by` |
| `publications` | Факт публикации тикета в чат: `ticket_id`, `chat_id`, `message_id` |
| `logs` | Журнал действий: `action`, `user_id`, `details` |

При старте (`init_db`) таблицы создаются и проставляются роли `admin` для всех `ADMIN_USER_IDS` (upsert - существующая роль не понижается).

---

## Роли и права

| Роль | Права |
|---|---|
| `user` | Отправка заявок, просмотр своей истории (`/my_history`), `/start`, `/help`, `/who_am_i` |
| `staff` | Всё выше + принятие и закрытие тикетов, `/chats`, `/republish_*`, `/all_history`, `/help_admins` |
| `admin` | Всё выше + `/set_role` |

Роли хранятся только в БД. Пользователь регистрируется с ролью `user` при первом `/start`. `ADMIN_USER_IDS` из `.env` сидируются в БД как `admin` при каждом старте.

---

## Жизненный цикл тикета

```
new -> публикация во все активные чаты
       staff нажимает "Принять" -> accepted
       staff нажимает "Завершить" -> done, уведомление пользователю
```

Медиавложения (фото, видео, аудио) сохраняются как `file_id` в `ticket_media` и пересылаются в чаты поддержки вместе с текстом тикета.

---

## Управление чатами поддержки

При добавлении бота в группу всем администраторам (`role = admin`) отправляется запрос на одобрение чата. Только одобренный и активный чат (`is_active = 1`) получает новые тикеты. Деактивация и повторная активация - через `/chats`.

---

## Команды

### Пользователь (`user`)

| Команда | Действие |
|---|---|
| `/start` | Регистрация, приветствие |
| `/help` | Краткая справка |
| `/who_am_i` | Telegram ID, username, роль |
| `/my_history` | История собственных заявок (статус, дата, текст) |
| любое сообщение | Создать тикет (текст / фото / видео / голос) |

### Staff и Admin

| Команда | Действие |
|---|---|
| `/chats` | Список всех чатов поддержки с кнопками активации/деактивации |
| `/republish_new_tickets` | Опубликовать все тикеты со статусом `new` во все активные чаты |
| `/republish_ticket <id>` | Переопубликовать тикет по ID независимо от статуса |
| `/all_history` | Полная история всех тикетов (разбивка по 4000 символов) |
| `/help_admins` | Расширенная справка |

### Только Admin

| Команда | Действие |
|---|---|
| `/set_role <telegram_id> <role>` | Назначить роль `user` / `staff` / `admin` |

---

## Конфигурация

Файл `.env` в корне проекта (создаётся автоматически с дефолтами при первом запуске, если отсутствует):

| Переменная | Обязательна | Дефолт | Описание |
|---|---|---|---|
| `BOT_TOKEN` | да | - | Токен бота (@BotFather) |
| `ADMIN_USER_IDS` | нет | `""` | Telegram user ID через запятую, получают роль `admin` при старте |
| `DATABASE_PATH` | нет | `/app/data/helpdesk.sqlite3` | Путь к файлу БД |
| `GTM_PLUS` | нет | `3` | Смещение часового пояса для отображения времени |
| `LOG_FILE` | нет | `bot.log` | Путь к файлу лога (WARNING+) |

---

## Логирование

- `INFO` и выше -- stdout (формат: `дата - уровень - сообщение`)
- `WARNING` и выше -- файл `LOG_FILE` (формат для `ERROR+`: `дата - уровень - [funcName] сообщение`)
- Уровень `aiogram.event` принудительно поднят до `WARNING`

---

## Запуск

### Docker (рекомендуется)

```sh
git clone https://github.com/Vadimohka/ASPZiZ_TechBot.git
cd ASPZiZ_TechBot

# Создать .env и заполнить BOT_TOKEN / ADMIN_USER_IDS
cp .env.example .env   # или создать вручную

docker compose up --build -d
```

БД (`helpdesk.sqlite3`) монтируется в `./data` - переживает пересборку образа.

### Без Docker

```sh
pip install -r requirements.txt
python main.py
```

Требуется Python 3.8+.

---

## Тесты

```sh
pip install pytest pytest-asyncio
pytest tests/
```

Тесты покрывают репозиторный слой: инициализацию БД, создание и смену статусов тикетов, upsert пользователей без понижения роли, трекинг публикаций.
