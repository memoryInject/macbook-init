import main as m


def test_dmg_install(monkeypatch):
    class FakeDMG:
        def __init__(self, url, confirm_msg):
            self.url = url

        def run(self):
            pass

    monkeypatch.setattr("main.DmgManagement", FakeDMG)
    monkeypatch.setattr("main.console", lambda: None)

    m.run_dmg_tasks([])  # Should not crash


def test_shell_exec(monkeypatch):
    calls = []

    def fake_shell(cmd, show_log=True, show_dialog=True):
        class Result:
            stderr = ""
            stdout = "ok"

        calls.append(cmd)
        return Result()

    monkeypatch.setattr("main.bash.run", fake_shell)
    monkeypatch.setattr("main.console.box", lambda title: None)

    m.run_bash_task("")

    assert len(calls) > 0
