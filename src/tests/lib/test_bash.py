import pytest
from pytest import MonkeyPatch
from lib.bash import run
from utils.errors import UserCancelled


def test_run_executes_subprocess():
    result = run("echo hi", show_log=True, show_dialog=True)

    assert result.stdout == "ok"
    assert result.stderr == ""


def test_run_skips_dialog_when_disabled():
    result = run("echo hi", show_dialog=False)

    assert result.stdout == "ok"


def test_run_raises_if_user_cancels(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("lib.bash.confirm", lambda prompt: False)
    with pytest.raises(UserCancelled):
        run("echo hi", show_dialog=True)
