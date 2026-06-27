import os
from pathlib import Path
from typing import Dict, List, Union

_ENCODING: str = "utf-8"

from dotenv import load_dotenv

_BOT_TOKEN_KEY: str = "BOT_TOKEN"
_ADMIN_IDS_KEY: str = "ADMIN_USER_IDS"
_GTM_PLUS_KEY: str = "GTM_PLUS"
_DATABASE_PATH_KEY: str = "DATABASE_PATH"
_LOG_FILE_KEY: str = "LOG_FILE"

_DEFAULT_DATABASE_PATH: str = "/app/data/helpdesk.sqlite3"
_DEFAULT_LOG_FILE: str = "bot.log"
_DEFAULT_GTM_PLUS: str = "3"

ENV_DEFAULTS: Dict[str, Union[str, int]] = {
    _BOT_TOKEN_KEY: "",
    _ADMIN_IDS_KEY: "",
    _GTM_PLUS_KEY: 3,
    _DATABASE_PATH_KEY: _DEFAULT_DATABASE_PATH,
    _LOG_FILE_KEY: _DEFAULT_LOG_FILE,
}

OPTIONAL_VALUES: List[str] = [_ADMIN_IDS_KEY, _LOG_FILE_KEY]


def _create_env_file() -> None:
    env_path = Path(".env")
    existing: Dict[str, str] = {}
    if env_path.exists():
        with open(str(env_path), "r", encoding=_ENCODING) as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and "=" in stripped:
                    key = stripped.split("=", 1)[0].strip()
                    existing[key] = ""
    with open(str(env_path), "a", encoding=_ENCODING) as f:
        for key, default in ENV_DEFAULTS.items():
            if key not in existing:
                f.write(f"{key}={default}\n")


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None or value == "":
        raise RuntimeError(f"{name} is not set")
    return value.strip()


_create_env_file()
load_dotenv()

TOKEN: str = _require_env(_BOT_TOKEN_KEY)
ADMIN_USER_IDS: List[int] = [
    int(i.strip())
    for i in os.environ.get(_ADMIN_IDS_KEY, "").split(",")
    if i.strip()
]
GTM_PLUS: int = int(os.environ.get(_GTM_PLUS_KEY, _DEFAULT_GTM_PLUS))
DATABASE_PATH: str = os.environ.get(_DATABASE_PATH_KEY, _DEFAULT_DATABASE_PATH)
DATABASE_DIR: str = str(Path(DATABASE_PATH).parent)
LOG_FILE: str = os.environ.get(_LOG_FILE_KEY, _DEFAULT_LOG_FILE)
