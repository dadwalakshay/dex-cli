import pytest
from rich.console import Console


@pytest.fixture(autouse=True)
def disable_rich_console_print(monkeypatch):
    def mock_rich_print():
        pass

    monkeypatch.setattr(Console, "print", lambda *args, **kwargs: mock_rich_print())
