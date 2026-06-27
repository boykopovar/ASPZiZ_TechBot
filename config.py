import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in .env file or environment!")

ADMIN_USER_IDS = [
    int(i.strip()) for i in os.getenv("ADMIN_USER_IDS", "").split(",") if i.strip()
]
GTM_PLUS: int = os.getenv("GTM_PLUS", 3)
# Абсолютный путь внутри контейнера (volume ./data:/app/data)
DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/data/helpdesk.sqlite3")
DATABASE_DIR = str(Path(DATABASE_PATH).parent)

# Только user_id в ADMIN_USER_IDS обладают абсолютной ролью admin!
