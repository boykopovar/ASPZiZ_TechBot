MSG_WELCOME: str = (
    "Добро пожаловать! Просто напишите свою заявку текстом, фото, видео или голосом. "
    "Для просмотра своих заявок используйте /my_history.\n"
    "Для помощи — /help."
)
MSG_HELP: str = (
    "<b>Доступные команды:</b>\n"
    "/help — показать справку\n"
    "/who_am_i — узнать свою роль и Telegram ID\n"
    "/my_history — посмотреть свои заявки\n"
    "Любое текстовое/медийное сообщение — создать заявку в поддержку"
)
MSG_HELP_ADMINS: str = """
<b>Админские и пользовательские команды Helpdesk-бота:</b>

<code>/start</code>
— Запускает бота, регистрирует пользователя с ролью <b>user</b>. После команды можно отправлять обращения (текст, фото, видео, голос).

<code>/who_am_i</code>
— Показывает ваш Telegram ID, username и роль в системе (роль всегда из базы данных).

<code>/my_history</code>
— Показывает все ваши обращения в систему: дата, статус (new/accepted/done), текст обращения. Для всех пользователей.

<code>/help</code>
— Краткая справка для пользователя.

<b>Только для staff или admin:</b>

<code>/chats</code>
— Список всех подключённых чатов поддержки. Можно включать/выключать чаты кнопками прямо из Telegram.

<code>/republish_new_tickets</code>
— Переотправляет все новые неразмещённые заявки во все активные чаты поддержки.

<code>/republish_ticket &lt;id&gt;</code>
— <b>Новая команда!</b> Переопубликовывает ЛЮБУЮ заявку по номеру (id) во все активные чаты поддержки, независимо от статуса и прошлых публикаций. Пример: <code>/republish_ticket 7</code>

<code>/all_history</code>
— Полная история всех заявок: номер, дата, статус, начало текста, отправитель. Если заявок много — разбивка по 4000 символов.

<code>/set_role &lt;user_id&gt; &lt;role&gt;</code>
— <b>Команда для админа!</b> Позволяет назначить роль user/staff/admin по Telegram ID.
Пример: <code>/set_role 123456 staff</code>
Пользователь должен быть в базе. Только для admin.

<b>Кнопки и callback-и (в чатах поддержки):</b>
• <b>Принять</b> — <b>Только staff</b> может взять заявку в работу (меняет статус на accepted, появляется подпись кто и когда взял).
• <b>Завершить</b> — Завершает заявку (статус done, приходит сообщение пользователю).

<b>Чат-менеджмент (только staff/admin):</b>
— При добавлении бота в новый чат, админам приходит запрос на одобрение/отклонение чата. Только после одобрения заявки из этого чата будут попадать в обработку.

<b>Прочее:</b>
• Все действия фиксируются в логах: создание, смена статуса, активация чатов, публикации и т.д.
• Роли (user, staff, admin) хранятся только в базе. Если пользователь появляется впервые — всегда "user" после /start.
• Только staff/admin могут управлять заявками, чатами, переотправлять заявки и видеть историю всех тикетов.

<b>Если нужна справка по конкретной команде — просто напиши её название в чат!</b>
"""
MSG_WHO_AM_I: str = (
    "Ваш Telegram ID: <code>{telegram_id}</code>\n"
    "Username: {username}\n"
    "Роль в системе: <b>{role}</b>"
)
MSG_NOT_REGISTERED: str = "Вы не зарегистрированы в системе.\nПоявитесь в базе после первой заявки."
MSG_NO_USER_TICKETS: str = "У вас пока нет заявок."
MSG_UNKNOWN_COMMAND: str = "Неизвестная команда. Введите /help для списка команд."
MSG_TICKET_RECEIVED: str = "Джинны творят магию, ожидайте!"
MSG_NO_TEXT: str = "(без текста)"
MSG_ONLY_STAFF: str = "Только staff может принять заявку."
MSG_TICKET_BUSY: str = "Заявка уже занята."
MSG_TICKET_NOT_FOUND: str = "Заявка не найдена."
MSG_TICKET_DONE_ANSWER: str = "Заявка завершена."
MSG_ACCEPT_NOTIFY_STAFF: str = "Вы взяли заявку #{ticket_id}:\n{ticket_text}\n{user_link}"
MSG_ACCEPT_NOTIFY_USER: str = (
    "Ваша заявка #{ticket_id} взята в работу сотрудником поддержки.\n"
    "{user_link} займётся вашим вопросом!"
)
MSG_DONE_NOTIFY_USER: str = "Ваша заявка #{ticket_id} успешно завершена! Спасибо за обращение."
MSG_ACCEPTED_SUFFIX: str = "\n\nПринял: {user_link} в {accept_time}"
MSG_ACCESS_DENIED_STAFF: str = "Доступ только для staff или admin."
MSG_ACCESS_DENIED_ADMIN: str = "Доступ только для админа."
MSG_NO_CHATS: str = "Нет подключённых чатов."
MSG_CHAT_ACTIVATED: str = "Чат активирован!"
MSG_CHAT_DEACTIVATED: str = "Чат деактивирован!"
MSG_CHAT_APPROVED: str = "Чат одобрен!"
MSG_CHAT_DECLINED: str = "Чат отклонён!"
MSG_NEW_CHAT_NOTIFY: str = "Новый чат добавлен: {title} (id: {chat_id}). Апрувить?"
MSG_REPUBLISH_COUNT: str = "Опубликовано новых заявок: {count}"
MSG_REPUBLISH_TICKET_COUNT: str = "Заявка #{ticket_id} переопубликована в {count} чат(ах)."
MSG_REPUBLISH_USAGE: str = "Используй: /republish_ticket <id_заявки>"
MSG_TICKET_NOT_FOUND_ID: str = "Заявка #{ticket_id} не найдена."
MSG_NO_TICKETS: str = "Заявок не найдено."
MSG_SET_ROLE_USAGE: str = "Использование: /set_role <telegram_id> <role>\nПример: /set_role 123456 staff"
MSG_ROLE_INVALID: str = "Роль должна быть одной из: user, staff, admin"
MSG_USER_NOT_FOUND: str = "Пользователь с Telegram ID {telegram_id} не найден."
MSG_ROLE_UPDATED: str = "Роль пользователя {telegram_id} изменена на {role}."
MSG_CHAT_STATUS_LINE: str = "{title} ({chat_id}): {status}\n"

BTN_ACCEPT: str = "Принять"
BTN_DONE: str = "Завершить"
BTN_APPROVE_CHAT: str = "✅ Одобрить"
BTN_DECLINE_CHAT: str = "🚫 Отклонить"
BTN_ACTIVATE_CHAT: str = "Активировать {title}"
BTN_DEACTIVATE_CHAT: str = "Деактивировать {title}"

CHAT_STATUS_ACTIVE: str = "✅ Активен"
CHAT_STATUS_INACTIVE: str = "❌ Неактивен"

ACCEPT_TIME_FMT: str = "%H:%M:%S"
TG_MAX_CHARS: int = 4000
SNIPPET_LEN: int = 50
SNIPPET_SUFFIX: str = "..."
USER_LINK_USERNAME: str = "@{username}"
USER_LINK_ID: str = "<a href='tg://user?id={uid}'>{name}</a>"
TICKET_LINE_HISTORY: str = "#{ticket_id} [{status}] — {snippet}"
TICKET_LINE_ALL: str = "#{ticket_id} [{status}] {created_at} — @{username}: {snippet}"
CAPTION_WITH_LINK: str = "{text}\n{user_link}"

CB_PREFIX_ACCEPT: str = "accept"
CB_PREFIX_DONE: str = "done"
CB_PREFIX_ACTIVATE_CHAT: str = "activate"
CB_PREFIX_DEACTIVATE_CHAT: str = "deactivate"
CB_PREFIX_APPROVE_CHAT: str = "approve_chat"
CB_PREFIX_DECLINE_CHAT: str = "decline_chat"

LOG_ACTION_ACCEPT: str = "accept_ticket"
LOG_ACTION_DONE: str = "done_ticket"
LOG_ACTION_ACTIVATE_CHAT: str = "activate_chat"
LOG_ACTION_DEACTIVATE_CHAT: str = "deactivate_chat"
