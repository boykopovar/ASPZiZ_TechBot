import pytest
import pytest_asyncio
import src.repositories.db_repository as repo
import src.env_tools as env_tools

@pytest_asyncio.fixture(autouse=True)
async def setup_db(tmp_path, monkeypatch):
    monkeypatch.setattr(repo, "DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.setattr(repo, "ADMIN_USER_IDS", [111])
    await repo.init_db()

@pytest.mark.asyncio
async def test_admin_seeded():
    user = await repo.get_user_by_id(111)
    assert user is not None
    assert user[3] == "admin"

@pytest.mark.asyncio
async def test_create_and_fetch_ticket():
    ticket_id = await repo.save_ticket(42, "testuser", "Проблема")
    ticket = await repo.get_ticket(ticket_id)
    assert ticket[3] == "Проблема"
    assert ticket[4] == "new"

@pytest.mark.asyncio
async def test_ticket_accept():
    ticket_id = await repo.save_ticket(42, "testuser", "Тест")
    await repo.set_ticket_accepted(ticket_id)
    ticket = await repo.get_ticket(ticket_id)
    assert ticket[4] == "accepted"

@pytest.mark.asyncio
async def test_ticket_done():
    ticket_id = await repo.save_ticket(42, "testuser", "Тест")
    await repo.set_ticket_done(ticket_id)
    ticket = await repo.get_ticket(ticket_id)
    assert ticket[4] == "done"

@pytest.mark.asyncio
async def test_publication_tracking():
    ticket_id = await repo.save_ticket(1, "u", "t")
    assert not await repo.is_ticket_published(ticket_id, 999)
    await repo.register_publication(ticket_id, 999, 1)
    assert await repo.is_ticket_published(ticket_id, 999)

@pytest.mark.asyncio
async def test_upsert_does_not_downgrade_admin():
    await repo.add_or_update_user(111, "newname")
    user = await repo.get_user_by_id(111)
    assert user[3] == "admin"
