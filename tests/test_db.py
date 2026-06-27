import pytest
import pytest_asyncio
from src.repositories import db_repository

@pytest_asyncio.fixture(autouse=True)
async def setup_db(tmp_path, monkeypatch):
    monkeypatch.setattr("src.repositories.db_repository.DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.setattr("src.env_tools.ADMIN_USER_IDS", [111])
    await db_repository.init_db()

@pytest.mark.asyncio
async def test_admin_seeded():
    user = await db_repository.get_user_by_id(111)
    assert user is not None and user[3] == "admin"

@pytest.mark.asyncio
async def test_create_ticket():
    ticket_id = await db_repository.save_ticket(42, "testuser", "Проблема")
    ticket = await db_repository.get_ticket(ticket_id)
    assert ticket[3] == "Проблема"
    assert ticket[4] == "new"
